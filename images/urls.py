from django.urls import path
from .views import ImageList, TemporaryLink, TemporaryLinkUse

urlpatterns = [
    path('', ImageList.as_view(), name='images'),
    path('get-link', TemporaryLink.as_view(), name='get_temporary_link'),
    path('temporary/<str:token>/', TemporaryLinkUse.as_view(), name='temporary_link')
]
