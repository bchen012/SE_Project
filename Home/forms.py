from django import forms
from django.forms import Form
from .models import Post
from .towns import TOWN_CHOICES
from .flats import FLAT_CHOICES


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['town', 'postal_code', 'address', 'floor_number', 'flat_type', 'floor_area', 'remaining_lease',
                  'price', 'recommended_price', 'description', 'display_image', 'gallery_image_0', 'gallery_image_1',
                  'gallery_image_2', 'gallery_image_3']


class FilterForm(Form):
    filter_town = forms.ChoiceField(choices=TOWN_CHOICES)
    filter_flat = forms.ChoiceField(choices=FLAT_CHOICES)
