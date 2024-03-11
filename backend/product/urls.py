from django.urls import path
from product.views import AddProduct, Products

urlpatterns = [
    path('addProduct/', AddProduct.as_view(), name='addProduct'),
    path('products/', Products.as_view(), name='products'),
]
