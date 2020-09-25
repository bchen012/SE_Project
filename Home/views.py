from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Post
from users.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from .forms import PostForm
from django.http import HttpResponseRedirect


class Main(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    login_url = 'login'
    template_name = 'Home/main.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['town', 'floor_number', 'address', 'rooms', 'price', 'display_image',
              'gallery_image_0', 'gallery_image_1', 'gallery_image_2',
              'gallery_image_3']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')


def postView(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    favorited = False
    if profile.favorites.filter(id=id).exists():
        favorited = True
    return render(request, 'Home/post_info.html', {'post': post, 'favorited': favorited})


def favoritePost(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    favorited = False
    if profile.favorites.filter(id=id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)
        favorited = True
    return render(request, 'Home/post_info.html', {'post': post, 'favorited': favorited})