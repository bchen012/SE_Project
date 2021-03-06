from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)

from .forms import MessageReplyForm, NewMessageForm, NewMessageFormMultiple
from .models import Thread

try:
    from account.decorators import login_required
except:  # noqa
    from django.contrib.auth.decorators import login_required


class InboxView(TemplateView):
    """
    View inbox thread list.
    """
    template_name = "pinax/messages/inbox.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        currentUser = self.request.user
        context = super().get_context_data(**kwargs)
        threads1 = Thread.ordered(Thread.deleted(currentUser))
        print(type(threads1))
        threads2 = Thread.ordered(Thread.inbox(currentUser))
        folder = "inbox"
        threads = threads1 + threads2

        context.update({
            "folder": folder,
            "threads": threads,
            "threads_unread": Thread.ordered(Thread.unread(currentUser)),
            "currentUser": currentUser,
        })
        return context


class ThreadView(UpdateView):
    """
    View a single Thread or POST a reply.
    """
    model = Thread
    form_class = MessageReplyForm
    context_object_name = "thread"
    template_name = "pinax/messages/thread_detail.html"
    # success_url = reverse_lazy("pinax_messages:inbox")
    # success_url = "thread_detail"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(userthread__user=self.request.user).distinct()
        return qs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
            "thread": self.object
        })
        # print(self.object.userthread_set)
        return kwargs

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return response

    # def get_context_data(self, **kwargs):


class MessageCreateView(CreateView):
    """
    Create a new thread message.
    """
    template_name = "pinax/messages/message_create.html"

    # def get(self, request, *args, **kwargs):
    #     context = {"listing": self.kwargs.get("listing")}
    #     return render(self.request, self.template_name, context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_class(self):
        if self.form_class is None:
            if self.kwargs.get("multiple", False):
                return NewMessageFormMultiple
        return NewMessageForm

    def get_initial(self):
        user_id = self.kwargs.get("user_id", None)
        listing = self.kwargs.get("listing")
        flat_type = self.kwargs.get("flat_type")
        if listing:
            subject = listing + " " + flat_type
        else:
            subject = flat_type
        # print(listing)
        if user_id is not None:
            user_id = [int(user_id)]
        elif "to_user" in self.request.GET and self.request.GET["to_user"].isdigit():
            user_id = map(int, self.request.GET.getlist("to_user"))
        if not self.kwargs.get("multiple", False) and user_id:
            user_id = user_id[0]
        return {"to_user": user_id, "subject": subject}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
        })
        return kwargs


class ThreadDeleteView(DeleteView):
    """
    Delete a thread.
    """
    model = Thread
    success_url = reverse_lazy("pinax_messages:inbox")
    template_name = "pinax/messages/thread_confirm_delete.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.userthread_set.filter(user=request.user).update(deleted=True)
        return HttpResponseRedirect(success_url)
