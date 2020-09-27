from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .towns import TOWN_CHOICES

FLAT_CHOICES = (('Studio Apartment', 'Studio Apartment'),
                ('2-Room Flat', '2-Room Flat'),
                ('3-Room Flat', '3-Room Flat'),
                ('4-Room Flat', '4-Room Flat'),
                ('5-Room Flat', '5-Room Flat'),
                ('Executive Flat', 'Executive Flat')
                )


class Post(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    town = models.CharField(max_length=25, choices=TOWN_CHOICES, default='ANG MO KIO')
    floor_number = models.IntegerField(default=0)
    postal_code = models.IntegerField(default=0)
    address = models.TextField(null=True)
    flat_type = models.CharField(max_length=20, choices=FLAT_CHOICES, default='2-Room Flat')
    floor_area = models.IntegerField(default=0)
    remaining_lease = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    recommended_price = models.IntegerField(default=0)
    description = models.TextField()
    display_image = models.ImageField(upload_to='home_images', default='default_home.png')
    gallery_image_0 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_1 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_2 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')
    gallery_image_3 = models.ImageField(null=True, upload_to='home_images', default='default_home.png')

    def __str__(self):
        return str(self.id)
