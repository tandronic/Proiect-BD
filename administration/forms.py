from django import forms

from users.models import User, alphanumeric, cnp_length


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    cnp = forms.CharField(max_length=40, validators=[alphanumeric, cnp_length])
    password = forms.CharField(max_length=40, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'cnp', 'password')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'dob')
