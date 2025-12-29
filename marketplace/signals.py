# AI Citation
# Description: First-time user welcome page 
# AI Use: Generated with ChatGPT on 2025-11-14.
#   Prompt: "I want to create a 'first time user page' that detects first-time sign in (new gmail logging in that hasn't logged in before) and directs them to a welcome page. How can i do this?"
# Notes: The AI generated the code below. I understand that the user_signed_up signal sent when the user first signs up is used to mark onboarding_complete as false if they are a new user.
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def mark_onboarding_needed(request, user, **kwargs):
    user.onboarding_complete = False
    user.save(update_fields=["onboarding_complete"])

