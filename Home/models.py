from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .towns import TOWN_CHOICES, TOWN_LIST
from .flats import FLAT_CHOICES, FLAT_LIST
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_town(value):
    if value not in TOWN_LIST:
        raise ValidationError(
            _('%(value)s is not a valid town'),
            params={'value': value},
        )


def validate_flat(value):
    if value not in FLAT_LIST:
        raise ValidationError(
            _('%(value)s is not a valid flat type'),
            params={'value': value},
        )


class Post(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    town = models.CharField(max_length=25, choices=TOWN_CHOICES, default='ANG MO KIO', validators=[validate_town])
    floor_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    postal_code = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999999)])
    address = models.TextField(blank=True, default='')
    flat_type = models.CharField(max_length=20, choices=FLAT_CHOICES, default='2-Room Flat', validators=[validate_flat])
    floor_area = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(200)])
    remaining_lease = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(99)])
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
