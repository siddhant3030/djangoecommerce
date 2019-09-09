from django.shortcuts import render
from product.models import Product
from satchmo_store.shop import signals
from satchmo_utils.signals import application_search

def search_view(request, template="shop/search.html"):
    """Perform a search based on keywords and categories in the form submission"""
    if request.method=="GET":
        data = request.GET
    else:
        data = request.POST

    keywords = data.get('keywords', '').split(' ')
    category = data.get('category', None)

    keywords = filter(None, keywords)

    results = {}
    
    # this signal will usually call listeners.default_product_search_listener
    application_search.send(Product, request=request, 
        category=category, keywords=keywords, results=results)

    context = {
            'results': results,
            'category' : category,
            'keywords' : keywords
    }
    return render(request, template, context)
