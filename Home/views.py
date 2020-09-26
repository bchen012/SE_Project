from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from users.models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
import requests
from sklearn import linear_model


class Main(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 1
    login_url = 'login'
    template_name = 'Home/main.html'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['town', 'address', 'floor_number', 'flat_type', 'floor_area', 'remaining_lease', 'price', 'description',
              'display_image', 'gallery_image_0', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')


def getData(town):
    data = requests.get(
        "https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=99999")
    data = json.loads(data.text)

    # Data Cleaning
    df = pd.DataFrame(data['result']['records'])
    df['storey_range'] = df.apply(lambda x: int(x['storey_range'][0:2]), axis=1)  # Simplify Story Range to the first 2 char only
    df = df[df['flat_type'] != 'MULTI-GENERATION']
    df['flat_type'] = df['flat_type'].apply(lambda x: '6 ROOM' if x == 'EXECUTIVE' else x)
    df['flat_type'] = df['flat_type'].apply(lambda x: x[:1].strip())
    df['remaining_lease'] = df['remaining_lease'].apply(lambda x: x[:2].strip())
    df = df.drop(columns=['flat_model', 'street_name', 'month', 'lease_commence_date', 'block', '_id'])
    df = df.loc[df['town'] == town]
    return df


def postView(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    favorited = False
    df = getData(post.town)
    X = df[['floor_area_sqm']]  # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
    Y = df['resale_price']
    # regr = linear_model.LinearRegression()
    # regr.fit(X, Y)
    fig = px.scatter(df, x='floor_area_sqm', y='resale_price', trendline='ols', trendline_color_override='darkblue', template='simple_white', opacity=0.9)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    if profile.favorites.filter(id=id).exists():
        favorited = True
    return render(request, 'Home/post_info.html', {'post': post, 'favorited': favorited, 'plot': plot_div})
# 'plot': plot_div


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