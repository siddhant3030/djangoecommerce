from django.shortcuts import render
from .models import Item

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)

def item_list(request):
    context = {
        'items': Item.Objects.all()
    }
    return render(request, "home-page.html", context)

def checkout(request):
    return render(request, "checkout.html")

