from django import forms
from .models import Listing, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'image']

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image", "username", "first_name", "last_name"]

# These are for CustomUser setup
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "image"]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "image"]