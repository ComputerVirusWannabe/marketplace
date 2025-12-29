from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import NoReverseMatch
from django.http import HttpResponseForbidden
from django.contrib import messages as dj_messages
from .models import Listing, Message, Chat, UserChat, CustomUser, Notification
from .forms import ListingForm, CustomUserEditForm
from django.http import HttpResponseForbidden
from django.contrib.auth import logout


from django.views.decorators.http import require_POST

def __is_moderator(user):
    return user.groups.filter(name="moderator").exists()

def __get_base_template(user):
    # Used for pages that can be accessed by both moderator or user
    if (__is_moderator(user)):
        return "marketplace/base_moderator.html"
    else:
        return "marketplace/base_user.html"
    
def __get_non_moderator_users(current_user, exclude_self = True):
    if (exclude_self):
        users = CustomUser.objects.exclude(id = current_user.id)
    else:
        users = CustomUser.objects.all()
    
    non_moderator_users = []
    
    for user in users:
        if (not __is_moderator(user)):
            non_moderator_users.append(user)

    return non_moderator_users

def __get_nickname(user):
    return user.nickname if hasattr(user, 'nickname') and user.nickname else user.username
    
def moderator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and __is_moderator(request.user): 
            return view_func(request, *args, **kwargs)
        return redirect('home') 
    return wrapper

def not_suspended(view_func):
    def wrapper(request, *args, **kwargs):
        if (request.user.is_suspended):
            logout(request)
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    return render(request, 'marketplace/home.html')

def explore(request):
    query = request.GET.get('q', '').strip()
    listings = Listing.objects.filter(available=True, visibility='public').order_by('-created_at')
    if query:
        listings = listings.filter(Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'listings': listings,
        'query': query,
    }
    return render(request, 'marketplace/explore.html', context)

@login_required
@not_suspended
def post_login(request):
    user = request.user

    if user.is_suspended:
        list(dj_messages.get_messages(request))  # Clear existing messages
        logout(request)
        dj_messages.error(request, "Your account has been suspended.")
        return redirect('home')
    # First-time onboarding
    if hasattr(user, 'onboarding_complete') and not user.onboarding_complete:
        return redirect('welcome')
    if __is_moderator(request.user):
        try:
            return redirect('moderator_home')
        except NoReverseMatch:
            return redirect('home')
    try:
        return redirect('user_home')
    except NoReverseMatch:
        return redirect('home')


# AI Citation
    # Description: The ability to filter listings based on categories, conditions, and owners. 
    # AI Use: Generated with ChatGPT on 2025-11-14.
    # Prompt: "Now I am adding a new feature: filtering by conditions/categories for user_home.html, which has all of the listings. I am thinking of creating a new page for filtering, and users will see checkboxes for each condition/category in order to filter the listings. Do you think it is a good plan?"
    # Notes: AI generated the idea to modify the code below. Essentially, it was adding selected_categories and selected_conditions as variables. AI generated a short code snippet to modify the code in user_home.html where it is a dropdown selection boxes to select desired categories and conditions. I integrated the idea with the existing search feature. 

@login_required
@not_suspended
def user_home(request):
    query = request.GET.get('q', '')

    selected_categories = request.GET.getlist('category')
    selected_conditions = request.GET.getlist('condition')

    listings = Listing.objects.filter(available=True)
    
    listings = listings.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__nickname__icontains=query)
    ).order_by('-created_at') if query else listings.order_by('-created_at')

    if selected_categories:
        listings = listings.filter(category__in=selected_categories)

    if selected_conditions:
        listings = listings.filter(condition__in=selected_conditions)

    context = {
        'category_choices': Listing.CATEGORY_CHOICES,
        'condition_choices': Listing.CONDITION_CHOICES,
        'selected_categories': selected_categories,
        'selected_conditions': selected_conditions,
        'listings': listings,
        'query': query,
    }
    return render(request, 'marketplace/user_home.html', context)

@login_required
@moderator_required
def moderator_home(request):
    return render(request, 'marketplace/moderator_home.html')

@login_required
@not_suspended
def add_listing(request):
    redirect_url = request.GET.get("redirect")  

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()    
            return redirect(redirect_url)       
    else:
        form = ListingForm()

    base_template = __get_base_template(request.user)
    return render(request, f'marketplace/add_listing.html', {'form': form, 'base_template': base_template})

@login_required
@not_suspended
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    base_template = __get_base_template(request.user)
    context = {
        'listing': listing, 
        'is_owner': listing.owner.id == request.user.id,
        'base_template': base_template,
        }
    return render(request, 'marketplace/listing_detail.html', context)


def public_listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    context = {'listing': listing}
    return render(request, 'marketplace/listing_detail_public.html', context)


@login_required
@not_suspended
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # refresh page after save
    else:
        form = CustomUserEditForm(instance=request.user)
    
    base_template = __get_base_template(request.user)
    context = {
        'form': form,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'nickname': request.user.nickname,
        'image': request.user.image,
        'biography': request.user.biography,
        'giving_away': request.user.giving_away.all(),
        'looking_for': request.user.looking_for.all(),
        'base_template': base_template,
    }
    
    return render(request, 'marketplace/user_profile.html', context)

# AI Citation
# Description: First-time user welcome page 
# AI Use: Generated with ChatGPT on 2025-11-14.
#   Prompt: " I want to create a 'first time user page' that detects first-time sign in (new gmail logging in that hasn't logged in before) and directs them to a welcome page. How can I do this?"
# Notes: I was told to add a welcome view with the following code, and have an onboarding_complete field which checks if the user has completed signup before. 
@login_required
@not_suspended
def welcome(request):
    if request.method == 'GET' and getattr(request.user, 'onboarding_complete', True):
        return redirect('post_login')

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            if not getattr(request.user, 'onboarding_complete', True):
                request.user.onboarding_complete = True
                request.user.save(update_fields=["onboarding_complete"])
            dj_messages.success(request, "Profile saved.")
                
    form = CustomUserEditForm(instance=request.user)
    first_name = request.user.first_name
    last_name = request.user.last_name

    context = {
        "form": form,
        "first_name":first_name,
        "last_name":last_name,
    }

    return render(request, 'marketplace/welcome.html', context)

@login_required
@not_suspended
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    
    base_template = __get_base_template(request.user)
    context = {
        'base_template':base_template
    }
    return render(request, 'marketplace/delete_account_confirm.html', context)

@login_required
@not_suspended
def user_public_profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    user_listings = Listing.objects.filter(owner=profile_user, available=True).order_by('-created_at')

    base_template = __get_base_template(request.user)
    context = {
        'profile_user': profile_user,
        'listings': user_listings,
        'base_template': base_template,
    }

    return render(request, 'marketplace/user_public_profile.html', context)

@login_required
@not_suspended
def my_listings(request):
    # navigate moderator away
    if (__is_moderator(request.user)):
        return redirect('moderator_listings')
    
    user = request.user
    query = request.GET.get('q', '')
    available = request.GET.get('available')
    
    if (available==None or available=="True"): 
        available = True
    else:
        available = False

    listings = Listing.objects.filter(owner=user, available=available)

    # Search filter
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )   
    listings = listings.order_by('-created_at')
    context = {
        'listings': listings,
        'query': query,
        'available': available,
    }
    return render(request, 'marketplace/my_listings.html', context)

@login_required
@moderator_required
def mod_listings(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('-created_at') if query else Listing.objects.order_by('-created_at')
    
    if request.GET.get('flagged') == "1":
        listings = listings.exclude(flagged_by__isnull=True)

    context = {
        'listings': listings,
        'query': query,
        'showing_flagged': request.GET.get('flagged') == "1",
    }
    return render(request, 'marketplace/moderator_listings.html', context)

# AI Citation
# Description: The ability to edit a listing in my_listings page
# AI Use: Generated with ChatGPT on 2025-10-30.
# Prompt: "I want to add the ability to edit a listing, how should I start."
# Notes: AI generated part of the code below. Since we already have a ListingForm, when users click the "edit" button, it sends a POST requst and users will be able to see fields with existing values in the edit view, just as if they are creating a new listing.

@login_required
@not_suspended
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    is_moderator = __is_moderator(request.user)

    if not is_moderator and listing.owner != request.user:
        return redirect("user_home")

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('my_listings') if not is_moderator else redirect("moderator_listings")
    else:
        form = ListingForm(instance=listing)

    base_template = __get_base_template(request.user)
    context = {
        'form': form,
        'is_moderator': is_moderator,
        'base_template': base_template
    }

    return render(request, 'marketplace/edit_listing.html', context)


# AI Citation
# Description: The ability to delete a listing in my_listings page
# AI Use: Generated with ChatGPT on 2025-10-31.
# Prompt: "Now I want to add the ability to delete a listing, similar to edit listings, there will be button for each listing. How can I implement that?"
# Notes: AI generated part of the code below. Very similar to edit listing. There is a delete confirmation page since this is a relatively dangerous operation. This view also checks if the current user is moderator or the owner of the listing. If not, user will be directed back to the home page with no changes done. 

@login_required
@not_suspended
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    is_moderator = __is_moderator(request.user)

    if not is_moderator and listing.owner != request.user:
        return redirect("user_home")
    
    if request.method == 'POST':
        listing.delete()

        if is_moderator:
            return redirect('moderator_listings')
        else:
            return redirect('my_listings')
    
    base_template = __get_base_template(request.user)
    context = {
        'listing': listing,
        'base_template': base_template
    }
        
    return render(request, 'marketplace/delete_confirmation.html', context)

# AI Citation
# Description: The ability to delete selected listings in my_listings page
# AI Use: Generated with ChatGPT on 2025-10-31.
# Prompt: "I want to be able to select the cards and delete them all. Explain how can I implement this."
# Notes: AI generated part of the code below. Added checkboxes in my_listings.html to allow the ability to send POST request with multiple listings (just ids). Then based on those IDs, get these listings and delete them one at the time. Once again, the user has to be moderator or the owner of the listings, or the delete will fail. 

@login_required
@not_suspended
def delete_selected(request):
    if request.method == "POST":

        selected_ids = request.POST.getlist('selected_listings')
        listings = Listing.objects.filter(id__in=selected_ids)

        if not listings:
            return redirect(request.META.get('HTTP_REFERER'))

        is_moderator = __is_moderator(request.user)

        if 'confirm' not in request.POST:
            return render(request, 'marketplace/delete_selected_confirm.html', {'listings': listings, 'base': 'marketplace/base_moderator.html' if is_moderator else 'marketplace/base_user.html', })

        for listing in listings:
            if is_moderator or listing.owner == request.user:
                listing.delete()
        
        if is_moderator:
            return redirect('moderator_listings')
        else:
            return redirect('my_listings')
        
    return HttpResponseForbidden("Invalid request")

@login_required 
@not_suspended 
def my_chats(request):
    # navigate moderator away
    if (__is_moderator(request.user)):
        return redirect('moderator_chats')

    user_chats = UserChat.objects.filter(user = request.user)
    chats = Chat.objects.filter(id__in=map(lambda user_chat : user_chat.chat.id, user_chats), active=True).order_by('-created_at')
    chats_by_me = chats.filter(created_by = request.user).exclude(is_custom_chat=True)
    chats_not_by_me = chats.exclude(created_by = request.user).exclude(is_custom_chat=True)
    users = __get_non_moderator_users(request.user, True)
    custom_chats = chats.filter(is_custom_chat=True)

    # Create a map of {chat: list of other users in the chat}
    other_user_chats = UserChat.objects.filter(chat__in=chats).exclude(user=request.user)
    other_user_map = {chat.id: [] for chat in chats}

    for user_chat in other_user_chats:
        other_user_map[user_chat.chat.id].append(user_chat.user)

    context = {
        'chats_by_me':chats_by_me,
        'chats_not_by_me':chats_not_by_me,
        'custom_chats':custom_chats,
        'other_user_map': other_user_map,
        'users': users,
    }

    return render(request, 'marketplace/my_chats.html', context)

@login_required 
@moderator_required
def moderator_chats(request):
    chats = Chat.objects.all().order_by('-created_at')
    custom_chats = chats.filter(is_custom_chat=True)
    item_request_chats = chats.filter(is_custom_chat=False)
    users = CustomUser.objects.all().exclude(id=request.user.id)

    # Create a map of {chat: list of users in the chat}
    user_chats = UserChat.objects.all()
    user_map = {chat.id: [] for chat in chats}

    for user_chat in user_chats:
        user_map[user_chat.chat.id].append(user_chat.user)

    if request.GET.get('showactive') == "1":
        item_request_chats = item_request_chats.exclude(active=False)
        show_active = True
    else:
        show_active = False

    context = {
        'item_request_chats':item_request_chats,
        'custom_chats':custom_chats,
        'user_map':user_map,
        'users':users,
        'show_active': show_active
    }

    return render(request, 'marketplace/moderator_chats.html', context)

@require_POST
@login_required
@not_suspended
def create_custom_chat(request):
    selected_user_ids = request.POST.getlist('selected_user_ids')
    chat_name = request.POST.get('chat-name-input')

    if (len(selected_user_ids) == 0 or chat_name == None):
        return redirect('my_chats')

    # Create chat
    new_chat = Chat.objects.create(created_by = request.user, name = chat_name, is_custom_chat = True) # no listing
    UserChat.objects.create(user = request.user, chat = new_chat)

    for user_id in selected_user_ids:
        added_user = CustomUser.objects.get(id=user_id)
        UserChat.objects.create(user = added_user, chat = new_chat)

        Notification.objects.create(
            user=added_user,
            type='custom_chat_invite',
            related_id=new_chat.id,
            message=f"{__get_nickname(request.user)} added you to a new custom chat: '{chat_name}'."
        )
    return redirect(f'/chat/{new_chat.id}/')

@login_required
@not_suspended  
def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)

    # Checking if user is allowed in the chat
    allowed_user_ids = UserChat.objects.filter(chat = chat).values_list("user", flat=True)
    if (request.user.id not in allowed_user_ids and not __is_moderator(request.user)):
        return redirect('user_home')
    
    messages = Message.objects.filter(chat_id = chat_id).order_by('created_at')
    base_template = __get_base_template(request.user)
    context = {
        'chat': chat, 
        'user':request.user, 
        'messages':messages,
        'base_template': base_template,
    }

    return render(request, 'marketplace/chat.html', context)

@login_required
@not_suspended
def create_chat(request):
    other_user_id = request.GET.get("user")
    other_user = CustomUser.objects.get(id=other_user_id)

    listing_id = request.GET.get("listing")
    listing = Listing.objects.get(id=listing_id)

    if (not listing.available):
        redirect(request.META.get('HTTP_REFERER'))

    # Check if chat already exists
    existing_chats = Chat.objects.filter(listing = listing_id) # Check that there are chats with this listing
    if (existing_chats):
        user_chat = UserChat.objects.filter(user = request.user.id, chat__in = existing_chats)
        if (user_chat): # Check that this user has the chat
            chat = user_chat.first().chat
            if (not chat.active):
                chat.active = True
                chat.save(update_fields=["active"])
            Notification.objects.create(
                user=other_user,
                type='item_request',
                related_id=chat.id,
                message=f"{__get_nickname(request.user)} has requested your listing '{listing.title}'."
            )
            return redirect(f'/chat/{chat.id}/')

    # Chat does not already exist
    new_chat = Chat.objects.create(listing = listing, created_by = request.user, name = f"Item Request for {listing.title}")
    UserChat.objects.create(user = other_user, chat = new_chat)
    UserChat.objects.create(user = request.user, chat = new_chat)

    Notification.objects.create(
        user=other_user,
        type='item_request',
        related_id=new_chat.id,
        message=f"{__get_nickname(request.user)} has requested your listing '{listing.title}'."
    )
    return redirect(f'/chat/{new_chat.id}/')

# AI Citation
# Description: The ability to flag a listing. 
# AI Use: Generated with ChatGPT on 2025-11-09.
# Prompt: "I want to add the ability to flag a listing for listings listed in listings.html. Explain the approach I should take."
# Notes: AI generated part of the code below. The AI gave multiple options, I selected the best one for this project. I also followed AI by adding a new attribute in Listing model called "flagged_by", which tracks a list of users flagged the listing. Within moderator_listing, I followed AI by added a filter option to display listing with at least one flagging. 

@login_required
@not_suspended
def flag_listing(request, listing_id):
    # Flags or unflags a listing
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.owner == request.user:
        return HttpResponseForbidden("Cannot flag your own listing.")
    
    if request.user in listing.flagged_by.all():
        # Unflag if flagged
        listing.flagged_by.remove(request.user)
        listing.save()
    else:
        # Flag if unflagged
        listing.flagged_by.add(request.user)
        listing.save()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@moderator_required
def moderator_flag_listing(request, listing_id):
    # Flags or unflags a listing
    listing = get_object_or_404(Listing, id=listing_id)

    if request.user in listing.flagged_by.all():
        # Unflag all
        listing.flagged_by.clear()
        listing.save()
    else:
        # Flag if unflagged
        listing.flagged_by.add(request.user)
        listing.save()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@moderator_required
def moderator_user_list(request):
    context = {'users': __get_non_moderator_users(request.user, True)}
    return render(request, 'marketplace/moderator_user_list.html', context)

@login_required
@moderator_required
@require_POST
def moderator_delete_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('moderator_user_list')

@login_required
@moderator_required
@require_POST
def moderator_create_chat(request, user_id):
    added_user = CustomUser.objects.get(id=user_id)

    # Look for existing chats
    chats = Chat.objects.filter(is_custom_chat = True, created_by = request.user)
    user_chat = UserChat.objects.filter(chat__in=chats, user = added_user)
    if (len(user_chat) == 2 and "Moderator Chat With" in user_chat.first().title):
        # Get existing chat
        new_chat = user_chat.first().chat
    else:
        # Create chat
        new_chat = Chat.objects.create(created_by = request.user, name = f"Moderator Chat With {request.user.nickname}", is_custom_chat = True)
        UserChat.objects.create(user = request.user, chat = new_chat)
        UserChat.objects.create(user = added_user, chat = new_chat)


    Notification.objects.create(
        user=added_user,
        type='custom_chat_invite',
        related_id=new_chat.id,
        message=f"A moderator, {request.user.nickname}, wants to chat with you."
    )
    return redirect(f'/chat/{new_chat.id}/')
        
@login_required
@moderator_required
@require_POST
def toggle_user_suspension(request, user_id):
    user_to_suspend = get_object_or_404(CustomUser, id=user_id)
    user_to_suspend.is_suspended = not user_to_suspend.is_suspended
    user_to_suspend.save()
    
    return redirect('moderator_user_list')

@login_required
@require_POST
@not_suspended
def accept_listing_request(request, listing_id, chat_id):
    accepted_chat = get_object_or_404(Chat, id=chat_id)

    if (accepted_chat.active): # Make sure chat wasn't canceled before the page reloaded
        listing = get_object_or_404(Listing, id=listing_id)

        # Set the chat to accepted
        accepted_chat.accepted = True
        accepted_chat.save(update_fields=["accepted"])
        
        # Set listing to unavailable
        listing.available = False
        listing.save(update_fields=["available"])
        
        # Get all active chats for this listing
        all_chats_excluding_accepted = Chat.objects.filter(listing=listing, active=True).exclude(id=chat_id)
        
        for chat in all_chats_excluding_accepted:
            # Mark all chats as inactive
            chat.active = False
            chat.save(update_fields=["active"])

            buyer = chat.created_by
            if buyer != request.user:
                if chat.id == accepted_chat.id:
                    # This request was accepted
                    Notification.objects.create(
                        user=buyer,
                        type='request_approved',
                        related_id=listing.id,
                        message=f"Good news! Your request for '{listing.title}' has been approved by {__get_nickname(request.user)}."
                    )
                else:
                    # Someone else got it, so this request is canceled
                    Notification.objects.create(
                        user=buyer,
                        type='request_status_change',
                        related_id=listing.id,
                        message=f"The listing '{listing.title}' is no longer available. Your request has been canceled."
                    )

        messages = Message.objects.filter(chat_id = chat_id).order_by('created_at')

        base_template = __get_base_template(request.user)
        context = {
            'chat': accepted_chat, 
            'user':request.user, 
            'messages':messages,
            'base_template':base_template
        }

        return render(request, 'marketplace/chat.html', context)
    else:
        return redirect('my_chats')

@login_required
@require_POST
@not_suspended
def cancel_listing_request(request, listing_id, chat_id):
    chat = get_object_or_404(Chat,id=chat_id)

    if (chat.active): # Make sure chat wasn't canceled before the page reloaded
        listing = get_object_or_404(Listing, id=listing_id)
        chat.active = False
        chat.accepted = False
        chat.save(update_fields=["active", "accepted"])

        listing.available = True
        listing.save(update_fields=["available"])
        
        #requester cancels
        if chat.listing.owner != request.user:
            Notification.objects.create(
                user=chat.listing.owner,
                type='request_canceled',
                related_id=chat.listing.id,
                message=f"{__get_nickname(request.user)} has canceled their request for '{chat.listing.title}'."
            )
        else: #owner cancels
            other_userchat = UserChat.objects.exclude(user = request.user).filter(chat = chat).get()
            Notification.objects.create(
                        user=other_userchat.user,
                        type='request_canceled',
                        related_id=chat.listing.id,
                        message=f"Your request for '{chat.listing.title}' has been canceled."
                    )
    return redirect('my_chats')

@login_required
@require_POST
@not_suspended
def finish_listing_request(request, chat_id):
    chat = get_object_or_404(Chat,id=chat_id)

    if (chat.active): # Make sure chat wasn't canceled before the page reloaded
        chat.active = False
        chat.save(update_fields=["active"])
        
        other_userchat = UserChat.objects.exclude(user = request.user).filter(chat = chat).get()
        Notification.objects.create(
                    user=other_userchat.user,
                    type='request_canceled',
                    related_id=chat.listing.id,
                    message=f"Your request for '{chat.listing.title}' has been finished."
                )
    
    return redirect('my_chats')

@login_required
def notifications_list(request):

    new_notifications = list(
        Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    )
    
    seen_notifications = list(Notification.objects.filter(
        user=request.user,
        is_read=True
    ).order_by('-created_at')[:20])

    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    context = {
        'new_notifications': new_notifications,
        'seen_notifications': seen_notifications,
        'new_count': len(new_notifications),
    }
    return render(request, 'marketplace/notifications_list.html', context)

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')
