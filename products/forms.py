from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    subject = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'write your review',
        'rows': 10,  
    }))
    rating = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Rate 1-5',
        'style': 'width: 200px; text-align: center;',
    }))

    class Meta:
        model = Review
        fields = ['rating', 'subject']
