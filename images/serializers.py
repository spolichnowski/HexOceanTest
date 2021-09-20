from rest_framework import serializers
from .models import CustomImageSize, ImageAPI
from rest_framework_simplejwt.tokens import RefreshToken


class ImageAPIBasicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = ImageAPI
        fields = ['image', 'thumbnail_200']


class ImageAPIPremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAPI
        fields = ['image', 'thumbnail_200', 'thumbnail_400']


class ImageAPIEnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAPI
        fields = ['image', 'thumbnail_200', 'thumbnail_400']


class CustomImageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomImageSize
        fields = ['custom_name', 'custom_height', 'custom_thumbnail']


class ImageAPICustomSerializer(serializers.ModelSerializer):
    custom_thumbnails = CustomImageSizeSerializer(many=True)

    class Meta:
        model = ImageAPI
        fields = ['image', 'thumbnail_200',
                  'thumbnail_400', 'custom_thumbnails']

    def create(self, validated_data):
        data = validated_data.pop('custom_thumbnails')
        image_api = ImageAPI.objects.create(**validated_data)
        for custom_image in data:
            CustomImageSize.objects.create(image_api=image_api, **custom_image)
        return image_api


class TemporaryLinkSerializer(serializers.Serializer):
    time_in_seconds = serializers.IntegerField()
