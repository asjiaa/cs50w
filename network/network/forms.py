from django import forms
from .models import Post

class ComposeForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "class": "form-control"}))