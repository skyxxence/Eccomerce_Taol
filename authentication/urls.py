from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerviewbuyer, name='go-register'),  # Registration page
    path('registerven/', registerviewvendor, name='go-register-vendor'),
    path('login/', loginview, name='go-login'), #login page
    path('profile/', profile_view, name='go-profile'),
    path('profile/edit/', edit_profile_view, name='go-edit-profile')
]
