from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserForm, ProfileUserForm
from .models import ProfileUser, CustomUser


# Create your views here.
def signup(request):
    user_form = CustomUserForm()
    profile_form = ProfileUserForm()
    if request.method == "POST":
        user_form = CustomUserForm(request.POST)
        profile_form = ProfileUserForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get("email")
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data["password"])
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")

    content = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "signup.html", content)


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def home(request):
    profile = ProfileUser.objects.get(user=request.user)
    content = {"profile": profile}
    return render(request, "home.html", content)
