"""
bughipster.bz_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import http
from django.views import generic
from django.views.generic.base import ContextMixin, View
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from bughipster.project import models as project_models
from bughipster.user import models as user_models
from . import forms


class Index(generic.TemplateView):
    template_name = 'bz_admin/index.html'


class Products(ContextMixin, View):
    template_engine = None
    response_class = TemplateResponse
    content_type = None
    template_name = 'bz_admin/products.html'

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.

        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def bz_add(self, request, *args, **kwargs):
        # TODO: add CC list and createseries
        form = forms.NewProduct(data=request.POST or None)
        context = self.get_context_data(form=form)
        if form.is_valid():
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
            return http.HttpResponseRedirect(
                reverse('back:products') +
                '?action=edit&product=%s' % product.name)
        if form.is_bound:
            message = form.get_message_from_errors() or repr(form.errors)
            context.update(message=message)
            return self.render_to_response(
                context=context,
                template='error.html',
            )
        return self.render_to_response(
            context=context,
            template='bz_admin/products/new.html',
        )

    def bz_edit(self, request, *args, **kwargs):
        context = self.get_context_data()
        product_name = request.GET.get('product', None)
        if product_name is None:
            context.update(
                message='You must select/enter a product.',
            )
            return self.render_to_response(
                context=context,
                template='error.html',
            )
        try:
            product = project_models.Product.objects.get(name=product_name)
        except project_models.Product.DoesNotExist:
            context.update(
                message="Either the product '%s' does not exist or you don't have access to it." % (product_name),
            )
            return self.render_to_response(
                context=context,
                template='error.html',
            )

        context.update(product=product)

        form = forms.EditProduct(data=request.POST or None, initial={
            'product': product.name,
            'description': product.description,
            'is_active': product.isactive,
            'allows_unconfirmed': product.allows_unconfirmed,
        })
        context.update(form=form)
        if form.is_valid():
            data = form.cleaned_data
            changes = {}

            if product.name != data['product']:
                changes['name'] = {
                    'old': product.name,
                    'new': data['product'],
                }
                product.name = data['product']

            if product.description != data['description']:
                changes['description'] = {
                    'old': product.description,
                    'new': data['description'],
                }
                product.description = data['description']

            isactive = data['is_active'] or False
            if product.isactive != isactive:
                changes['isactive'] = {
                    'old': product.isactive,
                    'new': isactive,
                }
                product.isactive = isactive

            allows_unconfirmed = data['allows_unconfirmed'] or False
            if product.allows_unconfirmed != allows_unconfirmed:
                changes['allows_unconfirmed'] = {
                    'old': product.allows_unconfirmed,
                    'new': allows_unconfirmed,
                }
                product.allows_unconfirmed = allows_unconfirmed

            product.save()
            context.update(changes=changes)

            return self.render_to_response(
                context=context,
                template='bz_admin/products/changes_summary.html',
            )

        if form.is_bound:
            message = form.get_message_from_errors() or repr(form.errors)
            context.update(message=message)
            return self.render_to_response(
                context=context,
                template='error.html',
            )

        return self.render_to_response(
            context=context,
            template='bz_admin/products/edit.html',
        )

    def bz_del(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            content_type=self.content_type,
        )

    def bz_showbugcounts(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            content_type=self.content_type,
        )

    def bz_show(self, request, *args, **kwargs):
        products = project_models.Product.objects.all()
        context = self.get_context_data(products=products)
        return self.response_class(
            request=self.request,
            template='bz_admin/products/list.html',
            context=context,
            using=self.template_engine,
            content_type=self.content_type,
        )

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', None)
        handler = self.bz_show
        if action == 'add':
            handler = self.bz_add
        elif action == 'edit':
            handler = self.bz_edit
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.GET.get('action', None)
        handler = self.bz_show
        if action == 'add':
            handler = self.bz_add
        elif action == 'edit':
            handler = self.bz_edit
        return handler(request, *args, **kwargs)
