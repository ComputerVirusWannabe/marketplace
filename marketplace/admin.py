from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Listing, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
CustomUserAdmin.fieldsets += ('Custom fields set', {'fields': ('image',)}),

admin.site.register(Listing)
admin.site.register(CustomUser, CustomUserAdmin)
