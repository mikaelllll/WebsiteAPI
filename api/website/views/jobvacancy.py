from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from api.models import JobVacancy

class JobVacancySignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = JobVacancy
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