from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("posts/<int:post_id>", views.PostView.as_view(), name='post'),
    path("post/<int:post_id>/delete", views.PostDeleteView.as_view(), name='post_delete'),
    path("posts/<int:post_id>/update", views.PostUpdateView.as_view(), name='post_update'),
    path("posts/create", views.PostCreateView.as_view(), name='post_create'),
]
