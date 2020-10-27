from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .towns import TOWN_CHOICES
from .flats import FLAT_CHOICES


class Post(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    town = models.CharField(max_length=25, choices=TOWN_CHOICES, default='ANG MO KIO')
    floor_number = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    postal_code = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    address = models.TextField(blank=True, default='')
    flat_type = models.CharField(max_length=20, choices=FLAT_CHOICES, default='2-Room Flat')
    floor_area = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    remaining_lease = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    recommended_price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    display_image = models.ImageField(upload_to='home_images', default='default_home.png')
    gallery_image_0 = models.ImageField(blank=True, upload_to='home_images', default='default_home.png')
    gallery_image_1 = models.ImageField(blank=True, upload_to='home_images', default='default_home.png')
    gallery_image_2 = models.ImageField(blank=True, upload_to='home_images', default='default_home.png')
    gallery_image_3 = models.ImageField(blank=True, upload_to='home_images', default='default_home.png')

    def __str__(self):
        return str(self.id)
