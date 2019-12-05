from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.utils import timezone

from .forms import SignUpForm, AdminUserSignUpForm, JobVacancySignUpForm, JobApplicationRegisterForm, CommentSignUpForm
from api.models import User, JobVacancy, JobApplication, Comment

#Function called when accessing the homepage 127.0.0.1:8000, and if the user is logged in it redirects the user tot the correct homepage
def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user or request.user.is_superuser:
            return redirect('admin_home')
        elif request.user.is_user_administrator:
            return redirect('user_admin_home')
        elif request.user.is_user_normal:
            return redirect('user_home')
    return render(request, 'website/home.html')

#Function tha redirects the request to the profile page and sends the data necessary to display the user information
#and if the user is a normal user it displays all the jobs he has applied to
def profile(request):
    job_applications = JobApplication.objects.filter(userID_id=request.user.id).all()
    job_vacancies = JobVacancy.objects.all()
    context = {'application_list':job_applications, 'job_list':job_vacancies}
    return render(request, 'website/profile.html', context)

#Function that redirects the request to the comment page for user administrators and sends all data necessary to see
#the user name that applied to the job and all comments that was made about the job applications
def comment(request, id):
    selected_company = JobVacancy.objects.filter(id = id).first()
    user_list = JobApplication.objects.filter(jobVacancyID_id = selected_company).all()
    all_user = User.objects.all()
    all_coments = Comment.objects.all()
    context = {'application_list':user_list, 'all_users':all_user, 'all_comment':all_coments}
    return render(request, 'website/comment.html', context)

#Function that redirects the request to the page that allows the creation of comments passing as argument the id of the selected user
#that the comment will be created for
def create_comment(request, companyid, userid):
    context = {'id': companyid, 'user':userid}
    return render(request, 'website/create_comment.html', context)

#Class that create the view for the signup form to register normal users
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

#Class that create the view for the signup form to register user administrators
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

#Class that helps creating the view to list all administrator users if you log in as a admin of the system
class ListAllAdminUser(ListView):
    template_name = 'website/admin_home.html'
    model = User
    context_object_name = "all_admin_users"

#Class that helps creating the view to register a job vacancy and register it in the database
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

#Class that helps creating the view to list all job vacanciy you have registered if you are logged in as user administrator
#Note: only shows the job vacancies you have registered, not other user administrators
class ListAllJobVacancy(ListView):
    template_name = 'website/user_admin_home.html'
    model = JobVacancy
    context_object_name = "all_job_vacancy"

    #Additional information passed to the page to associate the comment button to the correct job vacancy
    def get_context_data(self, **kwargs):
        ctx = super(ListAllJobVacancy, self).get_context_data(**kwargs)
        ctx['comments'] = Comment.objects.all()
        return ctx

#Class that helps creating the view to list all job vacanciy on the user home page and allowing the user to apply for the jobs
class ListAllJobVacancyUser(ListView):
    template_name = 'website/user_home.html'
    form_class =JobApplicationRegisterForm
    model = JobVacancy
    context_object_name = "all_job_vacancy"

    #Passing aditional information of all applications to handle wether the user already has a application to a certain job or nob
    def get_context_data(self, **kwargs):
        context = super(ListAllJobVacancyUser, self).get_context_data(**kwargs)
        context['applications'] = JobApplication.objects.filter()
        return context

    #Post handling for the user application to a job
    #If he clicks the 'apply' button it check if there is already a application from that user to the job that was not deleted
    #And if he clicks the 'remove application' button it sets the application as deleted in the database
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

#Class that helps creating the view to register a comment related to a specific job application
#The post method gets variables from the url link to know what user id is applying to what job
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