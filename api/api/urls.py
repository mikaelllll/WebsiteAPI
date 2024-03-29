"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from website import views

#Assigning all url paths of the application plus using the command to access static folder containing the .css for the html layouts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls', namespace='website')),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup_form/', views.UserSignUpView.as_view(), name='signup_form'),
    path('accounts/useradmin_signup_form/', views.AdminUserSignUpView.as_view(), name='useradmin_signup_form'),
    path('admin_home/', views.ListAllAdminUser.as_view(), name='admin_home'),
    path('user_admin_home/',views.ListAllJobVacancy.as_view(), name='user_admin_home'),
    path('user_home/', views.ListAllJobVacancyUser.as_view(), name='user_home'),
    path('registration/jobvacancy', views.JobVacancySignUpView.as_view(), name='register_job_vacancy'),
    path('comment/<id>/', views.comment, name='comment'),
    path('comment/<companyid>/<userid>/', views.CommentSignUp.as_view(), name='create_comment')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
