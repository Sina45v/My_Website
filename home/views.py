from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        posts = models.Post.objects.all()
        user = request.user
        return render(request, "home/home.html", context={"user":user, "posts":posts})

class PostView(View):
    def get(self, request, post_id):
        post = get_object_or_404(models.Post, pk=post_id)
        return render(request, "home/post.html", context={"post":post})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user.id == post.author.id:
            post.delete()
            messages.success(request, "Post deleted successfully")
        else:
            messages.error(request, "You do not have permission to delete this post")
        return redirect("account:profile", request.user.id)

class PostUpdateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm
    def setup(self, request, *args, **kwargs):
        self.userpost = get_object_or_404(models.Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.userpost.author.id:
            messages.error(request, "You do not have permission to edit this post")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.userpost)
        return render(request, "home/update.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.userpost)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect("account:profile", request.user.id)
        return render(request, "home/update.html", context={"form":form})

class PostCreateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, "home/createpost.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "Post created successfully")
            return redirect("account:profile", request.user.id)
        return render(request, "home/createpost.html", context={"form":form})