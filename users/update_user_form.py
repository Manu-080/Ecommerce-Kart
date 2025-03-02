from django import forms 
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']


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