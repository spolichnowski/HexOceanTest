from django.contrib import admin
from .models import CustomImageSize, ImageAPI

admin.site.register([CustomImageSize, ImageAPI])
