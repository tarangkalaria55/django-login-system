from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User as UserModel
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm  # Make sure to import your LoginForm
from django.conf import settings

from .forms import LoginForm

UserModel = get_user_model()


def user_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = UserModel.objects.get(username=data["username"])
                if user.check_password(data["password"]):
                    login(request, user)
                    return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
                else:
                    messages.error(request, "Invalid password.")
            except UserModel.DoesNotExist:
                messages.error(request, "User  does not exist.")

    return render(request, "account/login.html", {"form": form})


def logged_out(request: HttpRequest) -> HttpResponse:
    # logout(request)
    return render(request, "account/logged_out.html")


# @login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html")
