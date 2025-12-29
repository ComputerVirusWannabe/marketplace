from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(max_length=1000, blank=True, null=True)
    onboarding_complete = models.BooleanField(default=True, null=True)
    is_suspended = models.BooleanField(default=False)
    
    CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('clothes', 'Clothes'),
        ('makeup', 'Makeup'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('tools', 'Tools'),
        ('vehicles', 'Vehicles'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    ]
    
    giving_away = models.ManyToManyField('ListingCategory', related_name="giving_away", blank=True)
    looking_for = models.ManyToManyField('ListingCategory', related_name="looking_for", blank=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname

class ListingCategory(models.Model):
    code = models.CharField(max_length=20, choices=CustomUser.CATEGORY_CHOICES, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('clothes', 'Clothes'),
        ('makeup', 'Makeup'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('tools', 'Tools'),
        ('vehicles', 'Vehicles'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('broken', 'Broken'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Visible to everyone'),
        ('logged_in', 'Only visible to logged in users'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    image = models.ImageField(upload_to='listings/')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    flagged_by = models.ManyToManyField(CustomUser, related_name="flagged_listings", blank=True)
    available = models.BooleanField(default=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return self.title

class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', blank=True, null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length = 130, blank=True, null=True)
    is_custom_chat = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
    
class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chat}-{self.author}-{self.created_at}"
    
class UserChat(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chat}-{self.user}"
    
class Notification(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='notifications')
    TYPE_CHOICES = [
        ('item_request', 'Item Request Received'),
        ('request_approved', 'Request Approved'),
        ('request_canceled', 'Request Canceled'),
        ('request_status_change', 'Request Status Changed'),
        ('new_message', 'New Message in Chat'),
        ('suspension', 'Account Suspension'),
        ('custom_chat_invite', 'Added to Custom Chat'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    related_id = models.IntegerField(null=True, blank=True)  
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.nickname} - {self.type}"