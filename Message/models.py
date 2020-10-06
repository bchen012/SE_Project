from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    # conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    msg_content = models.TextField(null=True, )  # text field
    created_at = models.DateTimeField(default=timezone.now)  # time field

    def __str__(self):
        return self.msg_content
