from django.urls import path
from authentication.views import Test

urlpatterns = [
    path('test/', Test.as_view(), name='test'),
]
