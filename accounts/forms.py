from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class AccountsAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the acounts app.Extend this to get a form that accepts username/password logins.
    """

    # username = UsernameField(
    #     max_length=254,
    #     widget=forms.TextInput(attrs={'autofocus': True, 'class': ''}),
    # )
    # password = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput,
    # )

    error_messages = {
        'invalid_login': _(
            "Please enter the correct username and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    # def confirm_login_allowed(self, user):
    #     if not user.is_active or not user.is_staff:
    #         raise forms.ValidationError(
    #             self.error_messages['invalid_login'],
    #             code='invalid_login',
    #             params={'username': self.username_field.verbose_name}
    #         )