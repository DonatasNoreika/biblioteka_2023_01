from .models import BookReview, Profilis
from django import forms
from django.contrib.auth.models import User

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content', 'book', 'reviewer']
        widgets = {"book": forms.HiddenInput(), 'reviewer': forms.HiddenInput}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']

