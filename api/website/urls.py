from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
]