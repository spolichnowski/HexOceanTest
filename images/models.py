from django.db import models
from django.core.files.base import ContentFile

from .validators import validate_extension
from io import BytesIO
from PIL import Image
import os


class ImageAPI(models.Model):
    owner = models.ForeignKey(
        'auth.User', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/', validators=[validate_extension])
    thumbnail_200 = models.ImageField(
        upload_to='images/', blank=True, null=True, editable=False)
    thumbnail_400 = models.ImageField(
        upload_to='images/', blank=True, null=True, editable=False)

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        self.make_thumbnail(200)
        self.make_thumbnail(400)

        super(ImageAPI, self).save(*args, **kwargs)

    def make_thumbnail(self, height):
        width = self.image.width
        img = Image.open(self.image)
        img.thumbnail((height, width), Image.ANTIALIAS)

        # New path
        old_name, extension = os.path.splitext(self.image.name)
        name = f'{old_name}_thumbnail_{height}{extension}'

        # File type
        file_type = extension.replace('.', '').upper()
        if file_type == 'JPG':
            file_type = 'JPEG'

        thumbnail = BytesIO()
        img.save(thumbnail, file_type)
        thumbnail.seek(0)

        # Create thumbnail
        if height == 200:
            self.thumbnail_200.save(
                name, ContentFile(thumbnail.read()), save=False)
        elif height == 400:
            self.thumbnail_400.save(
                name, ContentFile(thumbnail.read()), save=False)

        thumbnail.close()
        return True


class CustomImageSize(models.Model):
    """Custom image size for custom users"""
    image_api = models.ForeignKey(
        ImageAPI, related_name='custom_thumbnails', on_delete=models.CASCADE)
    custom_height = models.IntegerField()
    custom_name = models.CharField(max_length=50, blank=True, editable=False)
    custom_thumbnail = models.ImageField(
        upload_to='images/', blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.custom_name = f'thumbnail_{self.custom_height}'
        self.make_custom_thumbnail(self.custom_height)
        super(CustomImageSize, self).save(*args, **kwargs)

    def make_custom_thumbnail(self, height):
        width = self.image_api.image.width
        print(self.image_api.image.url)
        img = Image.open(self.image_api.image.path)
        img.thumbnail((height, width), Image.ANTIALIAS)

        # New path
        old_name, extension = os.path.splitext(self.image_api.image.name)
        name = f'{old_name}_thumbnail_{height}{extension}'

        # File type
        file_type = extension.replace('.', '').upper()
        if file_type == 'JPG':
            file_type = 'JPEG'

        thumbnail = BytesIO()
        img.save(thumbnail, file_type)
        thumbnail.seek(0)

        # Create custom thumbnail
        self.custom_thumbnail.save(
            name, ContentFile(thumbnail.read()), save=False)

        thumbnail.close()
        return True
