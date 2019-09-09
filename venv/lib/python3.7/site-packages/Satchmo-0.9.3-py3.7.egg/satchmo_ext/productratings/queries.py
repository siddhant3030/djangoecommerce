"""Product queries using ratings."""
from django.conf import settings
import six
if 'django_comments' in settings.INSTALLED_APPS:
    from django_comments.models import Comment
else:
    from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from keyedcache import cache_get, cache_set, NotCachedError
from product.models import Product
from .utils import average
from .models import ProductRating
import logging
import math

log = logging.getLogger('product.comments.queries')

def highest_rated(count=0, site=None):
    """Get the most highly rated products"""
    if site is None:
        site = Site.objects.get_current()

    site_id = site.id

    try:
        pks = cache_get("BESTRATED", site=site_id, count=count)
        pks = [pk for pk in pks.split(',')]
        log.debug('retrieved highest rated products from cache')
        
    except NotCachedError as nce:
        # here were are going to do just one lookup for all product comments

        product_ratings = ProductRating.objects.rated_products().filter(comment__site__id=site_id).distinct().order_by('comment__object_pk')
        
        # then make lists of ratings for each
        commentdict = {}
        for rating in product_ratings:
            commentdict.setdefault(rating.comment.object_pk, []).append(rating.rating)
        
        # now take the average of each, and make a nice list suitable for sorting
        ratelist = [(average(ratings), pk) for pk, ratings in commentdict.items()]
        ratelist.sort()
        #log.debug(ratelist)
        
        # chop off the highest and reverse so highest is the first
        ratelist = ratelist[-count:]
        ratelist.reverse()

        pks = ["%s" % p[1] for p in ratelist]
        pkstring = ",".join(pks)
        log.debug('calculated highest rated products, set to cache: %s', pkstring)
        cache_set(nce.key, value=pkstring)
    
    products = []
    if pks:
        ids = []
        for pk in pks:
            try:
                _id = int(pk)
                ids.append(_id)
            except ValueError:
                pass
        productdict = Product.objects.in_bulk(ids)
        for _id in ids:
            try:
                products.append(productdict[_id])
            except KeyError:
                pass
    return products
