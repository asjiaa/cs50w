from django import forms
from .models import Listing

class CreateForm(forms.Form):
    category = forms.ChoiceField(choices=Listing.Category, widget=forms.Select(attrs={"class": "form-control"}))
    title = forms.CharField(label="Title ", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description ", widget=forms.Textarea(attrs={"class": "form-control"}))
    bid = forms.DecimalField(label="Starting Bid ",  widget=forms.NumberInput(attrs={"class": "form-control"}))
    image = forms.URLField(label="Image ", widget=forms.URLInput(attrs={"class": "form-control"}))

class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Bid", "class": "form-control"})
    )

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add Comment", "class": "form-control"}))