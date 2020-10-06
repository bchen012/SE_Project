from django.shortcuts import render
from .models import Message
from django.contrib.auth.models import User
from itertools import chain


def getConversations(request):
    received = Message.objects.filter(receiver=request.user)
    sent = Message.objects.filter(sender=request.user)



def getMessages(request):
    received = Message.objects.filter(receiver=request.user)
    sent = Message.objects.filter(sender=request.user)
    context = {'received': received, 'sent': sent}
    return render(request, 'Message/message_list.html', context)
