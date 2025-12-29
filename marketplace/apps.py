from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace'

    # AI Citation
    # Description: First-time user welcome page 
    # AI Use: Generated with ChatGPT on 2025-11-14.
    #   Prompt: "I want to create a 'first time user page' that detects first-time sign in (new gmail logging in that hasn't logged in before) and directs them to a welcome page. How can i do this?"
    # Notes: The AI generated the ready() function below. I understand that importing signals helps execute signals.py, which I need to detect the first-time user. 
    def ready(self) -> None:
        from . import signals
        return super().ready()

