from django import forms
from .models import Signup

class FormSignUp(forms.ModelForm):
    class Meta:
        model= Signup
        fields =['email','name']
    def clean_email(self):
        email =self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError("please enter gmail.com")

        return  email