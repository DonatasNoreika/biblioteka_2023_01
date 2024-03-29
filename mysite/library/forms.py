from .models import BookReview, Profilis, BookInstance
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

class DateInput(forms.DateInput):
    input_type = 'date'

class UserBookInstanceCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'reader', 'due_back', 'status']
        widgets = {'reader': forms.HiddenInput(), "due_back": DateInput()}