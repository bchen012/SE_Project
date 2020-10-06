from django.conf.urls import url
from django.urls import path
from . import views

app_name = "pinax_messages"

urlpatterns = [
    url(r"^inbox/$", views.InboxView.as_view(),
        name="inbox"),
    url(r"^create/$", views.MessageCreateView.as_view(),
        name="message_create"),
    path('create/<int:user_id>/<str:listing>/<str:flat_type>', views.MessageCreateView.as_view(),
        name="message_user_create"),
    url(r"^thread/(?P<pk>\d+)/$", views.ThreadView.as_view(),
        name="thread_detail"),
    url(r"^thread/(?P<pk>\d+)/delete/$", views.ThreadDeleteView.as_view(),
        name="thread_delete"),
]
