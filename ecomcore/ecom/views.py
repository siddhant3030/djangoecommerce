from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.shortcuts import redirect

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

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item_slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
    else: 
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect("ecom:product", kwarg={
        'slug': slug
     })


# def checkout(request):
#     return render(request, "checkout.html")

