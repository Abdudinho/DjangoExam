from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, ListView

from apps.forms import LoginForm
from apps.models import User, Post


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return redirect('register')
        if User.objects.filter(first_name=first_name).exists():
            return redirect("register")
        hashed_password = make_password(password)
        User.objects.create_user(username=username, password=hashed_password, first_name=first_name)
        return render(request, 'login.html', {"position": "login"})
    else:
        return render(request, 'register.html', {"position": "register"})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Email yoki parol noto'g'ri")
        return render(request, self.template_name)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "login"

class IndexTemplateView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['page'] = self.request.GET.get("page")
        return data

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'create_post.html'
    fields = ['title','content', 'is_published','views','author','created_at','updated_at']
    success_url = reverse_lazy('dashboard')

