from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterationForm

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('home')

        return render(request,'login.html', {"form":form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class RegisterView(View):
    def get(self, request):
        form = RegisterationForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('home')

        return render(request,'register.html', {"form":form})
    
class ForgotpasswordView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'forgot_password.html', {"form": form})
    
    def post(self, request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            print("fuck you")
            # return redirect('home')

        return render(request,'forgot_password.html', {"form":form})
