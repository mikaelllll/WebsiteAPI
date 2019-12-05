from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django import template
from django.utils import timezone

register = template.Library()

from .decorators import user_required
from .forms import SignUpForm, AdminUserSignUpForm, JobVacancySignUpForm, JobApplicationRegisterForm, UserChangeForm, CommentSignUpForm
from api.models import User, JobVacancy, JobApplication, Comment

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user or request.user.is_superuser:
            return redirect('admin_home')
        elif request.user.is_user_administrator:
            return redirect('user_admin_home')
        elif request.user.is_user_normal:
            return redirect('user_home')
    return render(request, 'website/home.html')

def profile(request):
    return render(request, 'website/profile.html')

def comment(request, id):
    selected_company = JobVacancy.objects.filter(id = id).first()
    user_list = JobApplication.objects.filter(jobVacancyID_id = selected_company).all()
    all_user = User.objects.all()
    all_coments = Comment.objects.all()
    context = {'application_list':user_list, 'all_users':all_user, 'all_comment':all_coments}
    return render(request, 'website/comment.html', context)

def create_comment(request, companyid, userid):
    context = {'id': companyid, 'user':userid}
    return render(request, 'website/create_comment.html', context)

class UserSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'website/signup_form.html'

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
    template_name = 'website/useradmin_signup_form.html'

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

    def get_context_data(self, **kwargs):
        ctx = super(ListAllJobVacancy, self).get_context_data(**kwargs)
        ctx['comments'] = Comment.objects.all()
        return ctx

class ListAllJobVacancyUser(ListView):
    template_name = 'website/user_home.html'
    form_class =JobApplicationRegisterForm
    model = JobVacancy
    context_object_name = "all_job_vacancy"

    def get_context_data(self, **kwargs):
        context = super(ListAllJobVacancyUser, self).get_context_data(**kwargs)
        context['applications'] = JobApplication.objects.filter()
        return context


    def post(self, request):
        if request.method == 'POST':
            if 'appliedJob' in request.POST:
                instance  = JobApplication(
                    jobVacancyID = JobVacancy.objects.filter(id=request.POST.get('id')).first(),
                    userID=User.objects.filter(id=request.user.id).first(),
                    isDeleted = False
                )

                search = JobApplication.objects.filter(
                    jobVacancyID = request.POST.get('id')).filter(
                        userID = User.objects.filter(id=request.user.id).first()
                ).filter(isDeleted = 0).first()

                if search is None:
                    instance.save()
            if 'removesAppliedJob' in request.POST:
                search = JobApplication.objects.filter(
                    jobVacancyID=request.POST.get('id')).filter(
                    userID=User.objects.filter(id=request.user.id).first()
                ).filter(isDeleted=0).first()
                if search is not None:
                    search.isDeleted = True
                    search.deleteDate = timezone.localtime(timezone.now())
                    search.save()


        return redirect('user_home')

class CommentSignUp(CreateView):
    template_name = 'website/create_comment.html'
    model = Comment
    form_class = CommentSignUpForm
    success_url = reverse_lazy("user_admin_home")

    def post(self, request, companyid, userid):
        form = CommentSignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.jobApplicationID = JobApplication.objects.filter(id=companyid).first()
            instance.userADMID = User.objects.filter(id=userid).first()
            instance.save()
        return redirect('user_admin_home')