from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django.urls import reverse
# from PIL import Image


class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    town = models.TextField(null=True)
    floor_number = models.IntegerField(default=0)
    address = models.TextField(null=True)
    price = models.TextField(default=0)
    rooms = models.IntegerField(default=2)
    display_image = models.ImageField(upload_to='home_images', default='default_home.png')
    gallery_image_0 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_1 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_2 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_3 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')

    def __str__(self):
        return str(self.id)
