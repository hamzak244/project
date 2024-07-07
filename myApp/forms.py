from django import forms
from .widgets import MultipleFileInput
from .models import User

class UploadFileForm(forms.Form):
    documents = forms.FileField(widget=MultipleFileInput)

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

