from django import forms
from .models import Article

class UpdateArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ['title', 'text']
  