from django.urls import path
from views import (product, checkout, HomeView)

app_name = 'ecom'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', checkout, name='checkout'),
    path('product/', product, name='product')
]

