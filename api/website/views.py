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
from .forms import SignUpForm, AdminUserSignUpForm, JobVacancySignUpForm, JobApplicationRegisterForm, UserChangeForm
from api.models import User, JobVacancy, JobApplication

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user:
            return redirect('admin_home')
        elif request.user.is_user_administrator:
            return redirect('user_admin_home')
        elif request.user.is_user_normal:
            return redirect('user_home')
    return render(request, 'website/home.html')

def profile(request):
    return render(request, 'website/profile.html')

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
        return redirect('user_home')

class AdminUserSignUpView(CreateView):
    model = User
    form_class = AdminUserSignUpForm
    template_name = 'registration/useradmin_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('admin_home')

class ListAllAdminUser(ListView):
    template_name = 'website/admin_home.html'
    model = User
    context_object_name = "all_admin_users"

class JobVacancySignUpView(CreateView):
    model = JobVacancy
    form_class = JobVacancySignUpForm
    template_name = 'website/register_job_vacancy.html'
    success_url = reverse_lazy("user_admin_home")

    def post(self, request):
        form = JobVacancySignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.userADMID_id = request.user.id
            instance.save()
        return redirect('user_admin_home')


class ListAllJobVacancy(ListView):
    template_name = 'website/user_admin_home.html'
    model = JobVacancy
    context_object_name = "all_job_vacancy"

class ListAllJobVacancyUser(ListView):
    template_name = 'website/user_home.html'
    form_class =JobApplicationRegisterForm
    model = JobVacancy
    context_object_name = "all_job_vacancy"


    def post(self, request):
        if request.method == 'POST':
            instance  = JobApplication(
                jobVacancyID = JobVacancy.objects.filter(id=request.POST.get('id')).first(),
                userID=User.objects.filter(id=request.user.id).first(),
                isDeleted = False
            )

            print (instance.userID)


            print (request.user.id)
            print (request.POST.get('id'))

            instance.save()


        return redirect('user_home')