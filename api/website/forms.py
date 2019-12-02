from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from api.models import User, JobVacancy
from django.forms import ModelForm
from django.utils import timezone

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

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user_normal = True
        user.save()
        return user

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

class AdminUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'username'
        ]


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user_administrator = True
        user.save()
        return user


class JobVacancySignUpForm(ModelForm):
    class Meta:
        model = JobVacancy
        fields = [
            'company',
            'description',
            'salary'
        ]