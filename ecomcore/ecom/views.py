from django.shortcuts import render
from .models import Item

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)
