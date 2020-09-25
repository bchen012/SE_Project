from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'town', 'floor_number', 'address', 'price', 'rooms',
                  'display_image', 'gallery_image_0', 'gallery_image_1', 'gallery_image_2',
                  'gallery_image_3')
