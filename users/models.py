# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


def user_directory_path(instance, filename):
    # file will be uploaded to static / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    contactNumber = models.CharField(default="", max_length=8)

    def __str__(self):
        return '%s %s' % (self.user.username, '\'s Profile')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 50 or img.width > 50:
            output_size = (50, 50)
            img.thumbnail(output_size)
            img.save(self.image.path)