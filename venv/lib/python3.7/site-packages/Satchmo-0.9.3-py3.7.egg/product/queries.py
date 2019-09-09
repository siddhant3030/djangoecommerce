from django.db.models import Count

from keyedcache import cache_get, cache_set, NotCachedError
from product.models import Product
import logging

log = logging.getLogger('product.queries')

def bestsellers(count):
    """Look up the bestselling products and return in a list"""        
    sellers = []
    cached = False
    try:
        pks = cache_get('BESTSELLERS', count=count)
        if pks:
            pks = [int(pk) for pk in pks.split(',')]
            productdict = Product.objects.in_bulk(pks)
            #log.debug(productdict)
            for pk in pks:
                try:
                    if (int(pk)) in productdict:
                        key = int(pk)
                    else:
                        continue
                    sellers.append(productdict[key])
                except ValueError:
                    pass
            
            log.debug('retrieved bestselling products from cache')
        cached = True    
    except NotCachedError:
        pass
    
    except ValueError:
        pass

    if not cached:
        products = Product.objects.active_by_site().annotate(item_count=Count('orderitem')) \
                                                   .filter(item_count__gt=0).order_by('-item_count')
        sellers = products[:count] 
        pks = ",".join(str(pk) for pk in products.values_list('pk', flat=True)[:count])
        log.debug('calculated bestselling %i products, set to cache: %s', count, pks)
        cache_set('BESTSELLERS', count=count, value=pks)
        
    return sellers
