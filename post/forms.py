from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from cloudinary.models import CloudinaryField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'ingredients', 'method', 'is_vegan', 'image')
        widgets = {
            'description': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
            'method': SummernoteWidget(),
        }