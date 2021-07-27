from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse


def AdminLogin(request):
    return render(request, "admin_templates/login_template.html")


def AdminLoginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, password=password, username=username)

    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request, "Invalid Login")
        return HttpResponseRedirect(reverse("admin_login"))


def AdminLogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return HttpResponseRedirect(reverse('admin_login'))
