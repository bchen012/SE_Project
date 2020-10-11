from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from users.models import Profile
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from plotly.offline import plot
import plotly.express as px
import json
import pandas as pd
import requests
from .forms import PostForm, FilterForm
from sklearn import linear_model
from django.views.generic.edit import FormView


class Main(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    login_url = 'login'
    template_name = 'Home/main.html'
    ordering = ['-date_posted']

    def get_queryset(self):
        filter_town = self.request.GET.get('filter_town')
        filter_flat = self.request.GET.get('filter_flat')
        print(filter_town)
        print(filter_flat)
        return Post.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] = Post.objects.all().order_by('-date_posted')
        context['form'] = FilterForm(initial={
            'filter_town': self.request.GET.get('filter_town', ''),
            'filter_flat': self.request.GET.get('filter_flat', ''),
        })
        user = self.request.user
        context['user'] = user
        return context


def createPost(request):
    address = ' '
    recommendedPrice = 0
    town = 'ANG MO KIO'
    flat_type = '2-Room Flat'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        town = form['town'].value()
        flat_type = form['flat_type'].value()
        floor_area = form['floor_area'].value()
        remaining_lease = form['remaining_lease'].value()
        recommendedPrice = getRecommendedPrice(town, flat_type, floor_area, remaining_lease)
        if 'postalCode' in request.POST or 'predictPrice' in request.POST:
            address = getAddress(form['postal_code'].value())
        if 'done' in request.POST:
            print(form.errors)

            if form.is_valid() and form.cleaned_data['address'] != '':
                form.cleaned_data['address'] = address
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('main')
    else:
        form = PostForm()
    return render(request, 'Home/post_form.html', {'form': form, 'address': address, 'selectedFlatType': flat_type,
                                                   'recommendedPrice': recommendedPrice, 'selectedTown': town})


def updatePost(request, id):
    post = get_object_or_404(Post, id=id)
    address = post.address
    recommendedPrice = post.recommended_price
    town = post.town
    flat_type = post.flat_type
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        town = form['town'].value()
        flat_type = form['flat_type'].value()
        floor_area = form['floor_area'].value()
        remaining_lease = form['remaining_lease'].value()
        recommendedPrice = getRecommendedPrice(town, flat_type, floor_area, remaining_lease)
        if 'postalCode' in request.POST or 'predictPrice' in request.POST:
            address = getAddress(form['postal_code'].value())
        if 'done' in request.POST:
            print(form.errors)
            if form.is_valid():
                form.cleaned_data['address'] = address
                form.save()
                return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'Home/post_form.html', {'form': form, 'post': post, 'address': address, 'selectedFlatType': flat_type,
                                                   'recommendedPrice': recommendedPrice, 'selectedTown': town})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/profile'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


def getRecommendedPrice(town, flat_type, floor_area, remaining_lease):
    if flat_type == 'Executive Flat':
        flat_type = '6'
    if flat_type == 'Studio Apartment':
        flat_type = '1'
    with open('static/LearningModel/FlatType') as file:
        X1 = json.loads(file.read())
    with open('static/LearningModel/FloorArea') as file:
        X2 = json.loads(file.read())
    with open('static/LearningModel/RemainingLease') as file:
        X3 = json.loads(file.read())
    with open('static/LearningModel/Intercept') as file:
        intercept = json.loads(file.read())
    price = round(X1[town] * int(flat_type[0]) + X2[town] * int(floor_area) + X3[town] * int(remaining_lease) + intercept[town], 0)
    if price < 0:
        price = 0
    return price


def getAddress(postalCode):
    data = requests.get("https://developers.onemap.sg/commonapi/search?searchVal="+str(postalCode)+"&returnGeom=Y&getAddrDetails=Y&pageNum=1")
    data = json.loads(data.text)
    if 'found' in data:
        if data['found']==0:
            return ''
    else:
        return ''
    addr = str(data['results'][0]['BLK_NO'])+" "+str(data['results'][0]['ROAD_NAME']+" SINGAPORE "+str(postalCode))
    return addr


def updateData(request):
    data = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=99999")
    data = json.loads(data.text)
    # Data Cleaning
    df = pd.DataFrame(data['result']['records'])
    df['storey_range'] = df.apply(lambda x: int(x['storey_range'][0:2]), axis=1)  # Simplify Story Range to the first 2 char only
    df = df[df['flat_type'] != 'MULTI-GENERATION']
    df['flat_type'] = df['flat_type'].apply(lambda x: '6 ROOM' if x == 'EXECUTIVE' else x)
    df['flat_type'] = df['flat_type'].apply(lambda x: x[:1].strip())
    df['remaining_lease'] = df['remaining_lease'].apply(lambda x: x[:2].strip())
    df = df.drop(columns=['flat_model', 'street_name', 'month', 'lease_commence_date', 'block', '_id'])
    X1 = {}
    X2 = {}
    X3 = {}
    intercept = {}
    for i in df['town'].unique():
        string = ''
        dataFrame = df.loc[df['town'] == i]

        if '/' not in i:
            string = i
        else:
            for j in i:
                if j == '/':
                    break
                string += j
        path = 'static/Dataframes/' + string
        dataFrame.to_csv(index=False, path_or_buf=path)

        X = dataFrame[['flat_type', 'floor_area_sqm', 'remaining_lease']]
        Y = dataFrame['resale_price']
        regr = linear_model.LinearRegression()
        regr.fit(X, Y)
        X1[string] = regr.coef_[0]
        X2[string] = regr.coef_[1]
        X3[string] = regr.coef_[2]
        intercept[string] = regr.intercept_
        p = ''
        p += '(\''
        p+= string
        p+= '\', \''
        p+= string
        p+= '\'),'
        print(p)

    with open('static/LearningModel/FlatType', 'w') as file:
        file.write(json.dumps(X1))  # use `json.loads` to do the reverse

    with open('static/LearningModel/FloorArea', 'w') as file:
        file.write(json.dumps(X2))  # use `json.loads` to do the reverse

    with open('static/LearningModel/RemainingLease', 'w') as file:
        file.write(json.dumps(X3))  # use `json.loads` to do the reverse

    with open('static/LearningModel/Intercept', 'w') as file:
        file.write(json.dumps(intercept))  # use `json.loads` to do the reverse
    return render(request, 'Home/update_complete.html')


def getData(town, type):
    path = 'static/Dataframes/' + town
    df = pd.read_csv(path)
    df = df.loc[df['flat_type'] == type]
    return df


def postView(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    favorited = False
    flat_type = post.flat_type
    if flat_type == 'Executive Flat':
        flat_type = '6'
    if flat_type == 'Studio Apartment':
        flat_type = '1'
    df = getData(post.town, int(flat_type[0]))

    fig1 = px.scatter(df, x='floor_area_sqm', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'floor_area_sqm': 'Floor Area (Square meters)', 'resale_price': 'Resale Price ($)'},
                      title="Floor Area vs Price")

    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)

    fig3 = px.scatter(df, x='remaining_lease', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'remaining_lease': 'Remaining Lease (Years)', 'resale_price': 'Resale Price ($)'},
                      title="Remaining Lease vs Price")

    plot_div3 = plot(fig3, output_type='div', include_plotlyjs=False)

    fig4 = px.scatter(df, x='storey_range', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'storey_range': 'Floor Level', 'resale_price': 'Resale Price ($)'},
                      title="Floor Level vs Price")

    plot_div4 = plot(fig4, output_type='div', include_plotlyjs=False)

    if profile.favorites.filter(id=id).exists():
        favorited = True
    return render(request, 'Home/post_info.html',
                  {'post': post, 'favorited': favorited, 'plot1': plot_div1,  'plot3': plot_div3, 'plot4': plot_div4})


def favoritePost(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    flat_type = post.flat_type
    if flat_type == 'Executive Flat':
        flat_type = '6'
    if flat_type == 'Studio Apartment':
        flat_type = '1'
    df = getData(post.town, int(flat_type[0]))

    fig1 = px.scatter(df, x='floor_area_sqm', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'floor_area_sqm': 'Floor Area (Square meters)', 'resale_price': 'Resale Price ($)'},
                      title="Floor Area vs Price")

    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)

    fig3 = px.scatter(df, x='remaining_lease', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'remaining_lease': 'Remaining Lease (Years)', 'resale_price': 'Resale Price ($)'},
                      title="Remaining Lease vs Price")

    plot_div3 = plot(fig3, output_type='div', include_plotlyjs=False)

    fig4 = px.scatter(df, x='storey_range', y='resale_price', template='simple_white',
                      opacity=1,
                      labels={'storey_range': 'Floor Level', 'resale_price': 'Resale Price ($)'},
                      title="Floor Level vs Price")

    plot_div4 = plot(fig4, output_type='div', include_plotlyjs=False)

    favorited = False
    if profile.favorites.filter(id=id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)
        favorited = True
    return render(request, 'Home/post_info.html', {'post': post, 'favorited': favorited,  'plot1': plot_div1,
                                                   'plot3': plot_div3, 'plot4': plot_div4})
