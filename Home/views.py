from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from users.models import Profile
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from plotly.offline import plot
import plotly.express as px
import json
import pandas as pd
import requests
from .forms import PostForm
from sklearn import linear_model
from .towns import TOWN_CHOICES


class Main(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    login_url = 'login'
    template_name = 'Home/main.html'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        user = self.request.user
        context['user'] = user
        return context


def createPost(request):
    address = ' '
    recommendedPrice = ' '
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if 'postalCode' in request.POST:
            address = getAddress(form['postal_code'].value())

        if 'predictPrice' in request.POST:
            town = form['town'].value()
            flat_type = form['flat_type'].value()
            floor_area = form['floor_area'].value()
            remaining_lease = form['remaining_lease'].value()
            recommendedPrice = getRecommendedPrice(town, flat_type, floor_area, remaining_lease)

        if 'done' in request.POST:
            if form.is_valid():
                form.cleaned_data['address'] = address
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

                return redirect('main')
    else:
        form = PostForm()
    return render(request, 'Home/post_form.html', {'form': form, 'address': address, 'recommendedPrice': recommendedPrice})


def getRecommendedPrice(town, flat_type, floor_area, remaining_lease):
    with open('static/LearningModel/FlatType') as file:
        X1 = json.loads(file.read())
    with open('static/LearningModel/FloorArea') as file:
        X2 = json.loads(file.read())
    with open('static/LearningModel/RemainingLease') as file:
        X3 = json.loads(file.read())
    with open('static/LearningModel/Intercept') as file:
        intercept = json.loads(file.read())
    price = round(X1[town] * int(flat_type[0]) + X2[town] * int(floor_area) + X3[town] * int(remaining_lease) + intercept[town], 2)
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


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['town', 'address', 'floor_number', 'flat_type', 'floor_area', 'remaining_lease', 'price', 'description',
#               'display_image', 'gallery_image_0', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3']
#
#     def form_valid(self, form):
#
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('main')


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

    df = getData(post.town, int(post.flat_type[0]))

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
    favorited = False
    if profile.favorites.filter(id=id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)
        favorited = True
    return render(request, 'Home/post_info.html', {'post': post, 'favorited': favorited})
