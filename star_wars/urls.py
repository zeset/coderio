from django.contrib import admin
from django.urls import path
from .views import get_character, rate_character

urlpatterns = [
    path('character/<int:pk>/', get_character, name='character'),
    path('character/<int:pk>/rating', rate_character, name='character-rating'),
]
