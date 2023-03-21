from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Not Chosen'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols':60, 'rows':10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('Too long title - above 200 symbols')
        
        return title
    
class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.CharField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':10}))
    captcha = CaptchaField()