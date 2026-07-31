from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, CreateView, DeleteView, DetailView

from apps.forms import RegisterForm, LoginForm, PostModelForm, CommentModelForm
from apps.mixin import AnonymousRequiredMixin, CustomLoginRequiredMixin
from apps.models import *

from apps.models import Post, Comment


class RegisterFormView(AnonymousRequiredMixin, FormView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.cleaned_data['user']
        authenticate(user)
        return super().form_valid(form)

class LoginFormView(AnonymousRequiredMixin, FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('login')


class HomeListView(CustomLoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'

class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'dashboard.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'



class PostCreateView(CustomLoginRequiredMixin, CreateView):
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')
    form_class = PostModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(CustomLoginRequiredMixin, DetailView):
    queryset = Post.objects.all()
    pk_url_kwarg = 'id'
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        comments = Comment.objects.filter(
            post=post
        )

        context['comments'] = comments

        return context

class CommentCreateView(CustomLoginRequiredMixin, CreateView):
    template_name = 'post_detail.html'
    form_class = CommentModelForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        current_post_id = self.kwargs.get(self.pk_url_kwarg)

        post_object = get_object_or_404(Post, id = current_post_id)

        form.instance.post = post_object
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        current_post_id = self.kwargs.get(self.pk_url_kwarg)
        return reverse_lazy('post-detail', kwargs={'id': current_post_id})