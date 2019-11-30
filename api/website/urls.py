from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import website, admin, user, useradmin

app_name = 'website'

urlpatterns = [
    path('', website.home, name='home'),
]