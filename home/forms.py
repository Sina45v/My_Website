from django import forms
from . import models



class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea-field',
                'placeholder': 'Write your content here',
                'rows': 10
            }),
        }



