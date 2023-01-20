from allauth.account.forms import LoginForm,PasswordField
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from django import forms

from allauth.utils import (
    build_absolute_uri,
    get_username_max_length,
    set_form_field_order,
)


class MyCustomLoginForm(LoginForm):

    #password = PasswordField(label=_("Password"), autocomplete="current-password")
    #remember = forms.BooleanField(label=_("Remember Me"), required=False)

    #user = None
    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "The e-mail address and/or password you specified are not correct."
        ),
        "username_password_mismatch": _(
            "The username and/or password you specified are not correct."
        ),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class':"form-control" , 'id':"floatingPassword"})


        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address: name@example.com"),
                    "autocomplete": "email",
                    'class':'form-control',
                    'id': 'floatingInput'
                }
            )
            login_field = forms.EmailField(label=_("E-mail"), widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(
                attrs={"placeholder": _("username"), "autocomplete": "username",                     'class':'form-control',
                    'id': 'floatingInput'}
            )
            login_field = forms.CharField(
                label=_("username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:
            assert (
                app_settings.AUTHENTICATION_METHOD
                == AuthenticationMethod.USERNAME_EMAIL
            )
            login_widget = forms.TextInput(
                attrs={"placeholder": _("Username or e-mail"), "autocomplete": "email",                     'class':'form-control',
                    'id': 'floatingInput'}
            )
            login_field = forms.CharField(
                label=pgettext("field label", "Login"), widget=login_widget
            )
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]