from django.urls import path
from views import (ItemDetailView, checkout, HomeView, add_to_cart)

app_name = 'ecom'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart')
]

