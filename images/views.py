import requests

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (TemporaryLinkSerializer, ImageAPIBasicSerializer,
                          ImageAPIPremiumSerializer, ImageAPIEnterpriseSerializer, ImageAPICustomSerializer)
from .models import ImageAPI


class ImageList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ImageAPI.objects.all()

    def get_queryset(self):
        return ImageAPI.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        user = self.request.user
        if user.profile.tier == 'BASIC':
            return ImageAPIBasicSerializer
        elif user.profile.tier == 'PREMIUM':
            return ImageAPIPremiumSerializer
        elif user.profile.tier == 'ENTERPRISE':
            return ImageAPIEnterpriseSerializer
        elif user.profile.tier == 'CUSTOM':
            return ImageAPICustomSerializer


class TemporaryLink(generics.GenericAPIView):
    serializer_class = TemporaryLinkSerializer

    def get(self, request):
        return Response({"Provide time"})

    def post(self, request):
        user = self.request.user
        if user.profile.tier == 'ENTERPRISE' or user.profile.tier == 'CUSTOM':
            try:
                time = int(request.data['time_in_seconds'])
                token = get_tokens_for_user(request.user, time)
                if time < 300 or time > 30000:
                    return Response({"Choose time between 300 and 30000 seconds."})
                link = f"http://localhost:8000/images/temporary/{token}"
                return Response({"Temporary Link": link, "Expiry": time})
            except:
                return Response({"Something went wrong."})
        return Response({"No permission."})


class TemporaryLinkUse(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        token = f'Bearer {token}'
        url = "http://localhost:8000/images/"
        headers = {"Authorization": token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Response(response.content)
        else:
            return Response({"Something went wrong"})


def get_tokens_for_user(user, exp):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token.set_exp(lifetime=timedelta(seconds=exp))

    return str(refresh.access_token)
