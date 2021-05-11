from django import forms
from django.contrib.auth import password_validation
from django.contrib import messages
from django.utils.translation import ugettext as _


class ResetPasswordForm(forms.Form):
    password = forms.CharField( 
                    label=_('Password'),
                    max_length=100,

                    widget=forms.PasswordInput(
                        attrs={
                            'id': 'password',
                            'class': 'form-control',
                            'autocomplete': 'off',
                            'required': True}
                    ))
    confirm_password = forms.CharField( 
                    label=_('Confirm password'),
                    max_length=100, 
                    widget=forms.PasswordInput(
                         attrs={
                            'id': 'confirm_password',
                            'class': 'form-control',
                            'autocomplete': 'off',
                            'required': True}
                    ))
    token = forms.CharField(max_length=1000, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(_('Passwords do not match.'))

        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password', error)