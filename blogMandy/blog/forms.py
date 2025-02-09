from django import forms
from .models import Category,Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','image','category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('category name is already in the database')
        return name 