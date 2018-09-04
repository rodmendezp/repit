import uuid
from django import forms
from django.utils.translation import ugettext_lazy
from backend.models import User


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

    # TODO: CHANGE THIS, THIS IS KIND OF DUMB
    def get_unique_username(self):
        name = str(uuid.uuid1())
        if User.objects.filter(username=name).count() == 0:
            return name
        else:
            return self.get_unique_username()

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
        if not instance.has_usable_password():
            instance.set_password(self.cleaned_data['password'])
            instance.save()
        instance.send_activation()
        return instance

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
