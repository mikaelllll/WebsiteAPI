from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
]