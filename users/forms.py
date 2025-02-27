from django import forms 
from .models import User


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm password',
        'class' : 'form-control'
    }))
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'phone_number']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


        placeholders = {
            'first_name':'Enter your First name',
            'last_name':'Enter your last name',
            'phone_number':'Enter phone number',
            'email':'Enter Email'
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and confirm_password != password:
            self.add_error('confirm_password', 'passwords do not match')
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(' A user with this email already exists ')
        return email
        