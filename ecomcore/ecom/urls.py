from django.urls import path
from views import item_list

app_name = 'ecom'

urlpatterns = [
    path('', item_list, name='item-list')
]

