from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError
from api.models import User, JobVacancy, JobApplication, Comment
from django.forms import ModelForm
from django.utils import timezone

#SignUpForm is the form that helps in creating the normal user that will use the system to apply for jobs
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'cpf'
        ]

    #The save is atomic to prevent updates to the database occurring only partially
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user_normal = True
        user.save()
        return user

    #These methods are to make sure that in the page the user attributes label that are requires shows with a * in their names and it
    #also ensures that they are not left blank
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["last_name"]

    def clean_email(self):
        if self.cleaned_data["email"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["email"]

    def clean_telephone(self):
        if self.cleaned_data["telephone"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["telephone"]

    def clean_cpf(self):
        if self.cleaned_data["cpf"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["cpf"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name*"
        self.fields['last_name'].label = "Last Name*"
        self.fields['email'].label = "Email*"
        self.fields['telephone'].label = "Telephone"
        self.fields['cpf'].label = "CPF"


#AdminUserSignUpForm is the form that helps in creating user administrators that will register jobs in the system for users to apply to them
class AdminUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'username',
            'email'
        ]

    # The save is atomic to prevent updates to the database occurring only partially
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user_administrator = True
        user.save()
        return user

#JobVacancySignUpForm is the form that helps the users administrators to create new jobs for the application to list
class JobVacancySignUpForm(ModelForm):
    class Meta:
        model = JobVacancy
        fields = [
            'company',
            'description',
            'salary'
        ]


#JobApplicationRegisterForm is the form that helps to create a relation between user and job to know that the user has applied to a specific job
class JobApplicationRegisterForm(ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'jobVacancyID',
            'userID'
        ]

#CommentSignUpForm is the form that helps to create comment to a job application
class CommentSignUpForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]