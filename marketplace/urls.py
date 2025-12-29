from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),                       # Main homepage
    path('explore/', views.explore, name="explore"),         # Public explore page
    path('post-login/', views.post_login, name="post_login"),# Redirect after login
    path('welcome/', views.welcome, name='welcome'),
    path('user-home/', views.user_home, name="user_home"),   # listings page
    path('moderator-home/', views.moderator_home, name="moderator_home"),
    path('add-listing/', views.add_listing, name="add_listing"), # Add new listing page
    path('user-profile/', views.user_profile, name="user_profile"),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('user/<int:user_id>/', views.user_public_profile, name='user_public_profile'),  #View other users' profiles
    path('my-listings/', views.my_listings, name="my_listings"),
    path('moderator-listings/', views.mod_listings, name="moderator_listings"),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('public/listing/<int:listing_id>/', views.public_listing_detail, name='public_listing_detail'),
    path('listing/edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('listing/delete/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('listing/delete-selected', views.delete_selected, name='delete_selected'),
    path('listing/flag/<int:listing_id>/', views.flag_listing, name='flag_listing'),
    path('listing/<int:listing_id>/accept/<int:chat_id>/', views.accept_listing_request, name='accept_listing_request'),
    path('listing/<int:listing_id>/cancel/<int:chat_id>/', views.cancel_listing_request, name='cancel_listing_request'),
    path('listing/<int:chat_id>/finish/', views.finish_listing_request, name='finish_listing_request'),
    path('moderator/users/', views.moderator_user_list, name='moderator_user_list'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('moderator/suspend/<int:user_id>/', views.toggle_user_suspension, name='toggle_user_suspension'),
    path('moderator/delete-account/<int:user_id>/', views.moderator_delete_account, name='moderator_delete_account'),
    path('moderator/create-chat/<int:user_id>/', views.moderator_create_chat, name='moderator_create_chat'),
    path('moderator-listings/flag/<int:listing_id>/', views.moderator_flag_listing, name='moderator_flag_listing'),
    path('moderator-chats/', views.moderator_chats, name="moderator_chats"),

    # Messaging
    path('my-chats/', views.my_chats, name="my_chats"),
    path('my-chats/create-custom-chat', views.create_custom_chat, name="create_custom_chat"),
    path('chat/<int:chat_id>/', views.chat, name='chat'),
    path('create-chat/', views.create_chat, name='create_chat'),
]
