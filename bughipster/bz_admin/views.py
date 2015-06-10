"""
bughipster.bz_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django.views import generic
from bughipster.project import models as project_models
from bughipster.user import models as user_models
from . import forms


class BaseMixin(object):
    def render_to_response(self, context, **response_kwargs):
        """
        Slightly change the default `render_to_response` to handle an
        optional template keyword argument.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=response_kwargs.pop(
                'template',
                self.get_template_names()),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class Index(generic.TemplateView):
    template_name = 'bz_admin/index.html'


class ProductList(generic.ListView):
    template_name = "bz_admin/products/list.html"

    def get_queryset(self):
        return project_models.Product.objects.all()


class NewProduct(BaseMixin, generic.FormView):
    form_class = forms.NewProduct
    template_name = 'bz_admin/products/new.html'

    def form_valid(self, form):
        data = form.cleaned_data
        product = project_models.Product.objects.create(
            name=data['product'],
            description=data['description'],
            isactive=data['is_active'] or False,
            allows_unconfirmed=data['allows_unconfirmed'] or False,
            )
        # TODO: handle whenever a user doesn't exist.
        # This shouldn't happen but we never know

        owner = user_models.Profile.objects.get(
            login_name=data['initialowner'])
        project_models.Version.objects.create(
            value=data['version'],
            product=product)
        project_models.Component.objects.create(
            name=data['component'],
            product=product,
            owner=owner,
            description=data['comp_desc'])
        return self.render_to_response(
            self.get_context_data(
                form=form,
                product=product,
            ),
            template='bz_admin/products/edit.html',
        )

    def form_invalid(self, form):
        if form.is_bound:
            print('Message: %s' % form.get_message_from_errors())
            print(form.errors.keys())
            message = form.get_message_from_errors() or repr(form.errors)
            return self.render_to_response(
                context=self.get_context_data(
                    form=form,
                    message=message,
                ),
                template='error.html',
            )
        return self.render_to_response(self.get_context_data(form=form))


class EditProduct(BaseMixin, generic.FormView):
    form_class = forms.EditProduct
    template_name = 'bz_admin/products/edit.html'

    def get_project(self, request):
        product_name = request.GET.get('product', None)
        if product_name is None:
            raise LookupError('You must select/enter a product.')
        try:
            self.product = project_models.Product.objects.get(
                name=product_name)
        except project_models.Product.DoesNotExist:
            raise ValueError(
                "Either the product '%s' does not exist or "
                "you don't have access to it." % (product_name),
            )
        # TODO: access check

    def _change_attr(self, product, name, new_value):
        old_value = getattr(product, name)
        if old_value != new_value:
            setattr(product, name, new_value)
            return {
                name: {
                    'old': old_value,
                    'new': new_value,
                }
            }
        return {}

    def form_valid(self, form, *args, **kwargs):
        data = form.cleaned_data
        product = self.product
        changes = {}

        changes.update(self._change_attr(
            product, 'name',
            data['product']))
        changes.update(self._change_attr(
            product, 'description',
            data['description']))
        changes.update(self._change_attr(
            product, 'isactive',
            data['is_active'] or False))
        changes.update(self._change_attr(
            product, 'allows_unconfirmed',
            data['allows_unconfirmed'] or False))
        product.save()

        return self.render_to_response(
            context=self.get_context_data(
                form=form,
                product=self.product,
                changes=changes),
            template='bz_admin/products/changes_summary.html',
        )

    def form_invalid(self, form, *args, **kwargs):
        message = form.get_message_from_errors() or repr(form.errors)
        return self.render_to_response(
            context=self.get_context_data(
                form=form,
                product=self.product,
                message=message),
            template='error.html',
        )

    def get_initial(self):
        return {
            'product': self.product.name,
            'description': self.product.description,
            'is_active': self.product.isactive,
            'allows_unconfirmed': self.product.allows_unconfirmed,
        }

    def get(self, request, *arg, **kwarg):
        try:
            self.get_project(request)
        except (LookupError, ValueError) as e:
            return self.render_to_response(
                context=self.get_context_data(message=e.args[0]),
                template='error.html',
            )
        form = self.get_form()

        return self.render_to_response(self.get_context_data(
            form=form, product=self.product))

    def post(self, request, *args, **kwargs):
        try:
            self.get_project(request)
        except (LookupError, ValueError) as e:
            return self.render_to_response(
                context=self.get_context_data(message=e.message),
                template='error.html',
            )
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteProduct(BaseMixin, generic.FormView):
    template_name = 'bz_admin/products/confirm_delete.html'

    def get_product(self):
        product_name = self.request.GET.get('product', None)
        return project_models.Product.objects.get(name=product_name)

    def handle_product_does_not_exist(self):
        message = "You must select/enter a product."
        if self.request.GET.get('product', None):
            message = (
                "Either the product '%s' does not exist or you don't have "
                "access to it." % self.request.GET.get('product')
            )
        return self.render_to_response(
            context={
                'message': message,
            },
            template='error.html',
        )

    def get(self, request, *args, **kwargs):
        try:
            product = self.get_product()
        except project_models.Product.DoesNotExist:
            return self.handle_product_does_not_exist()
        return self.render_to_response(self.get_context_data(product=product))


def products(request, *args, **kwargs):
    action = request.GET.get('action', None)
    handler = ProductList.as_view()
    if action == 'add':
        handler = NewProduct.as_view()
    elif action == 'edit':
        handler = EditProduct.as_view()
    elif action == 'del':
        handler = DeleteProduct.as_view()
    return handler(request, *args, **kwargs)


#
# Components
#

class SelectProduct(BaseMixin, generic.ListView):
    model = project_models.Product
    context_object_name = 'products'
    template_name = 'bz_admin/components/product_choice.html'


class ComponentList(BaseMixin, generic.ListView):
    template_name = 'bz_admin/components/component_list.html'
    context_object_name = 'components'

    def get_product(self):
        if hasattr(self, '_product'):
            return self._product
        self._product = None
        product_name = self.request.GET.get('product')
        if product_name:
            try:
                self._product = project_models.Product.objects.get(
                    name=product_name)
            except project_models.Product.DoesNotExist:
                pass
        return self._product

    def get_context_data(self, **kwargs):
        print('GET_CONTEXT_DATA')
        kwargs = super(ComponentList, self).get_context_data(**kwargs)
        kwargs.update({'product': self.get_product()})
        print(kwargs)
        return kwargs

    def get_queryset(self):
        product_name = self.request.GET.get('product')
        return project_models.Component.objects.filter(
            product__name=product_name)


def components(request, *args, **kwargs):
    action = request.GET.get('action', None)
    handler = SelectProduct.as_view()
    if request.GET.get('product', None):
        # TODO: access permissions to the provided project
        # TODO: ensure the project name exists
        handler = ComponentList.as_view()
    return handler(request, *args, **kwargs)
