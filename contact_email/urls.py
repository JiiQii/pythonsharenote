from django.contrib import admin
from django.urls import path

from .views import emailView

urlpatterns = [
    path('email/', emailView, name='email'),

]
