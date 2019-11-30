from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup_form.html'


def home(request):
    return render(request, 'website/home.html')