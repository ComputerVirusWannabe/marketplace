from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),                       # Main homepage
    path('explore/', views.explore, name="explore"),         # Public explore page
    path('post-login/', views.post_login, name="post_login"),# Redirect after login
    path('user-home/', views.user_home, name="user_home"),   # listings page
    path('moderator-home/', views.moderator_home, name="moderator_home"),
    path('add-listing/', views.add_listing, name="add_listing"), # Add new listing page
    path('user-profile/', views.user_profile, name="user_profile"),
]
