from django.urls import path
from .views import *

urlpatterns = [
    path('', list_products, name='product'),
    path('create/', create_product, name='add_product'),
]