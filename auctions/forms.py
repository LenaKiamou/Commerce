from django.forms import ModelForm
from django import forms
from .models import *

class NewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'image', 'description', 'starting_bid', 'category']


class BidForm(ModelForm):
    value_offer = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    class Meta:
        model = Bids
        fields = ['value_offer']


class CommentForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "textarea", "placeholder": "Write a comment..."}))
    class Meta:
        model = Comments
        fields = ['content']
