from django.shortcuts import render
from .models import Post, HomeImages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse


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
    fields = ['town', 'floor_number', 'address', 'rooms', 'price', 'display_image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')


