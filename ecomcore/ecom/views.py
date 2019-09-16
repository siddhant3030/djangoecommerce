from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.shortcuts import redirect
from django.utils import timezone

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

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html',)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("/")
    
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item_slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else: 
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("ecom:product", slug=slug)

@login_required
def remove_from_cart(reqest, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_slug=item.slug).exists():
            OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove.(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("ecom:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecom:product", slug=slug)
    else:
        messages.info(request, "You do not have any orders")
         return redirect("ecom:product", slug=slug)
    

@login_required
def remove_single_item_from_cart(reqest, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_slug=item.slug).exists():
            OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            order.items.remove.(order_item)
            messages.info(request, "The item quantity was updated")
            return redirect("ecom:order-summary", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecom:product", slug=slug)
    else:
        messages.info(request, "You do not have any orders")
         return redirect("ecom:product", slug=slug)
    
# def checkout(request):
#     return render(request, "checkout.html")

