"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from Home import views as home_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('main/', home_views.Main.as_view(), name='main'),
    path('post/new/', home_views.createPost, name='post-create'),
    path('profile/', user_views.profile, name='profile'),
    path('user-profile/<str:username>', user_views.users_profile, name='users-profile'),
    path('view_post/<int:id>', home_views.postView, name='view_post'),
    path('favorite/<int:id>', home_views.favoritePost, name='favorite'),
    path('unfavorite/<int:id>', user_views.unfavorite, name='unfavorite'),
    path('updateStats/', home_views.updateData, name='updateData'),
    path('post/<int:id>/update', home_views.updatePost, name='post-update'),
    path('post/<int:pk>/delete', home_views.PostDeleteView.as_view(), name='post-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
