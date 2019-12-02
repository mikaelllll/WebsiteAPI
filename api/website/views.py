from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from .decorators import user_required
from .forms import SignUpForm, AdminUserSignUpForm
from api.models import User

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user:
            return redirect('admin_home')
    return render(request, 'website/home.html')

class UserSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class AdminUserSignUpView(CreateView):
    model = User
    form_class = AdminUserSignUpForm
    template_name = 'registration/useradmin_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('home')

class ListAllAdminUser(ListView):
    template_name = 'website/admin_home.html'
    model = User
    context_object_name = "all_admin_users"