from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from home.models import Post
from . import forms
from home import models

class UserRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    form_class = forms.UserRegisterForm
    template_name = 'account/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form":form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(username=clean_data['username'],email=clean_data['email'],password=clean_data['password'])
            messages.success(request, 'Account created successfully', "success")
            return redirect('home:home')
        return render(request, self.template_name, context={"form":form})

class UserLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    form_class = forms.UserLoginForm
    template_name = 'account/login.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form":form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'logged in successfully', "success")
                return redirect('home:home')
            messages.error(request, 'Username or password is incorrect', "error")
        return render(request, self.template_name, context={"form":form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully', "success")
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(author=user)
        if len(posts) == 0:
            posts = False
        return render(request, "account/profile.html", context={"user":user, "posts":posts})
