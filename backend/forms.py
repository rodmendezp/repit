import uuid
from django import forms
from backend.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy
from django.contrib.auth.forms import AuthenticationForm


class LoginEmailForm(AuthenticationForm):
    email = forms.EmailField()
    # User name is defined automatically later
    username = None
    backend = 'backend.auth.EmailBackend'

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    last_name = forms.CharField(label=ugettext_lazy('Last Name'), strip=True, widget=forms.TextInput, required=False)
    confirm_password = forms.CharField(label=ugettext_lazy('Password Confirmation'),
                                       strip=False, widget=forms.PasswordInput, min_length=8)
    error_message = {
        'invalid_confirmations': ugettext_lazy('Your confirmation password does not match, please try again'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(RegisterForm, self).__init__(*args, **kwargs)

    @staticmethod
    def get_unique_username():
        return str(uuid.uuid1())

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                self.error_message['invalid_confirmations'],
                code='invalid_confirmation',
            )
        return self.cleaned_data

    def save(self, commit=True):
        obj = self.instance
        if not obj.pk:
            obj.username = self.get_unique_username()
        instance = super(RegisterForm, self).save(commit)
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        instance.send_activation()
        return instance

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
