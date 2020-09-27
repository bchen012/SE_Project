from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['town', 'postal_code', 'address', 'floor_number', 'flat_type', 'floor_area', 'remaining_lease',
                  'price', 'recommended_price', 'description', 'display_image', 'gallery_image_0', 'gallery_image_1',
                  'gallery_image_2', 'gallery_image_3']
