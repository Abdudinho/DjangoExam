from django.urls import path
from django.views import View

from apps.views import IndexTemplateView, PostDetailView, \
    PostCreateView, register_view, DashboardView, LoginView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/register", register_view, name="register"),
    path('', IndexTemplateView.as_view(), name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create', PostCreateView.as_view(), name='post_create'),

]