from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib import messages
from .forms import RegisterationForm
from account.models import Account

from django.contrib.auth import authenticate

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/account/")
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('home')

        print(form.cleaned_data)
        return render(request,'login.html', {"form":form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/account/")
        else:
            form = RegisterationForm()
            return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterationForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    newUser = form.save()
                    # create main account for user and add user to group
                    Account.objects.create(name="main", user=newUser)
                    userGroup = Group.objects.get(name='user') 
                    userGroup.user_set.add(newUser)

                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password2']
                    user = authenticate(username=username, password=password)
                    login(request,user)
                    return redirect('home')
            except Exception as e:
                messages.error(request, "Something went wrong during registration. Please try again.")
                return redirect('registration')

        return render(request,'register.html', {"form":form})
