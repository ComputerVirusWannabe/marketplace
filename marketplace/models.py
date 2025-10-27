from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return self.username

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

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
