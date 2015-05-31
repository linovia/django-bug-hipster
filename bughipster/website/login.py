"""
bughipster.website.login
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import http
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


# Basically, the LoginForm is the django.auth.contrib.forms.AuthenticationForm
# which has been changed to match the bugzilla field names.
# The LoginForm class is under Copyright (c) Django Software Foundation and
# individual contributors.
class AuthenticationForm(forms.Form):
    Bugzilla_login = forms.CharField(max_length=254)
    Bugzilla_password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        if self.fields['Bugzilla_login'].label is None:
            self.fields['Bugzilla_login'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('Bugzilla_login')
        password = self.cleaned_data.get('Bugzilla_password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class LoginMixin(object):
    def post(self, request, *args, **kwargs):
        if 'GoAheadAndLogIn' in request.POST:
            login_form = AuthenticationForm(request.POST)
            # TODO: Log in
            if login_form.is_valid():
                print('VALID')
                return http.HttpResponseRedirect(request.get_full_path())

            print('Form errors: %s' % login_form.errors)

            # We failed to login. Warn the user to go back ala Bugzilla style
            context = self.get_context_data(
                title="Invalid Username Or Password", **kwargs)
            return self.response_class(
                request=self.request,
                template="login-failed.html",
                context=context,
                using=self.template_engine)

        # By default, just call the parent class
        return super(LoginMixin, self).post(request, *args, **kwargs)
