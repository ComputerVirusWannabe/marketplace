from django import forms
from .models import Listing, Message, Chat, UserChat, CustomUser, ListingCategory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category','condition', 'image', 'visibility']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'content', 'chat']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['listing']

class UserChatForm(forms.ModelForm):
    class Meta:
        model = UserChat
        fields = ['user', 'chat']

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image", "nickname", "biography", "giving_away", "looking_for"]
        widgets = {
            "giving_away": forms.CheckboxSelectMultiple(),
            "looking_for": forms.CheckboxSelectMultiple(),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "image"]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "image"]


class WelcomeProfileForm(forms.ModelForm):
    looking_for = forms.ModelMultipleChoiceField(
        queryset=ListingCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    giving_away = forms.ModelMultipleChoiceField(
        queryset=ListingCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "nickname", "biography", "looking_for", "giving_away", "image"]

    # AI Citation
    # Description: First-time profile setup: uneditable name from Google login
    # AI Use: Generated with GitHub Copilot on 2025-11-14.
    #   Prompt: “For the profile setup, the first name and last name should be the same as the google account used to log in and cannot be changed by the user. How can I do this?”
    # Notes: Copilot generated the code below. I understand it displays first_name and last_name as read only values populated by Django allauth from Google, preventing edits in signup
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].disabled = True
        self.fields["last_name"].disabled = True
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False

