from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import NoReverseMatch
from .models import Listing
from .forms import ListingForm, CustomUserEditForm


def home(request):
    return render(request, 'marketplace/home.html')

def explore(request):
    return render(request, 'marketplace/explore.html')

@login_required
def post_login(request):
    user = request.user
    if user.groups.filter(name='moderator').exists():
        try:
            return redirect('moderator_home')
        except NoReverseMatch:
            return redirect('home')
    try:
        return redirect('user_home')
    except NoReverseMatch:
        return redirect('home')

@login_required
def user_home(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('-created_at') if query else Listing.objects.all().order_by('-created_at')

    context = {
        'listings': listings,
        'query': query,
    }
    return render(request, 'marketplace/listings.html', context)

@login_required
def moderator_home(request):
    """Moderator's home page"""
    return render(request, 'marketplace/moderator_home.html')

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('user_home')
    else:
        form = ListingForm()
    return render(request, 'marketplace/add_listing.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserEditForm()
    form = CustomUserEditForm(initial={
        'username':request.user.username,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
    })
    
    context = {
        'form':form,
        'email':request.user.email,
        'image':request.user.image,
    }
    
    return render(request, 'marketplace/user_profile.html', context)
