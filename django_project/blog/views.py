from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


# Initial function who render the home view. It was replaced by PostListView class
def home(request):
    context = {
        'posts': Post.objects.all()[:5],
        'lastes': Post.objects.all().order_by('-id')[:3]
    }
    return render(request, 'blog/home.html', context)


class SlideBar:
    lastes = Post.objects.all().order_by('-date_posted')[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lastes'] = self.lastes
        return context


class PostListView(SlideBar, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # pagination functionality (from django.core.paginator import Paginator)


class UserPostListView(SlideBar, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # pagination functionality (from django.core.paginator import Paginator)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(SlideBar, DetailView):
    model = Post


class PostCreateView(SlideBar, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(SlideBar, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(SlideBar, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {
        'title': 'About this blog',
        'lastes': Post.objects.all().order_by('-id')[:3],
    }
    return render(request, 'blog/about.html', context)
