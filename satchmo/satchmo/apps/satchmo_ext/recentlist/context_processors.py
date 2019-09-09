from livesettings.functions import config_value
from product.models import Product

def recent_products(request):
    """Puts the recently-viewed products in the page variables"""
    recent = request.session.get('RECENTLIST',[])
    maxrecent = config_value('PRODUCT','RECENT_MAX')
    products = Product.objects.active_by_site().filter(
        slug__in = recent[:maxrecent]).prefetch_related('productimage_set')    
    return {'recent_products' : products}
    
