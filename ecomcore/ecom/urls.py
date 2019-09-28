from django.urls import path
from .views import (
ItemDetailView,
CheckoutView,
HomeView,
add_to_cart,
remove_from_cart, 
OrderSummaryView, 
remove_single_item_from_cart
)

app_name = 'ecom'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('order-summary/<slug>/', OrderSummaryView.as_view(), name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
]

