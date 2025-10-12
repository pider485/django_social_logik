from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = Profile
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2', })


class RegisterForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'username', 'phone', 'avatar', 'birth_date', 'password1', 'password2']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2', })

        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'})