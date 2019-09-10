from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def home(request):
    context = {
        'items': Item.Objects.all()
    }
    return render(request, "home-page.html", context)

class HomeView(ListView):
    model = Item
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def checkout(request):
    return render(request, "checkout.html")

