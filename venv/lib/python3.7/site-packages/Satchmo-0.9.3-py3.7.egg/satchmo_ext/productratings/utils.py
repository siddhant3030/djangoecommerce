from django.conf import settings
from six.moves import reduce
try:
    from django.contrib.comments.models import Comment
except ImportError:
    from django_comments.models import Comment
from django.contrib.sites.models import Site
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from .models import ProductRating
import logging
import operator

log = logging.getLogger('product.comments.utils')

def average(ratings):
    if ratings:
        return float(sum(ratings)) / len(ratings)

def get_product_rating(product, site=None):
    """Get the average product rating"""
    if site is None:
        site = Site.objects.get_current()

    rating = ProductRating.objects.rated_products().filter(comment__object_pk=product.pk, comment__site__id=site.pk) \
                                                   .distinct().aggregate(average=Avg('rating'))['average']
    log.debug("Rating: %s", rating)
    return rating

def get_product_rating_string(product, site=None):
    """Get the average product rating as a string, for use in templates"""
    rating = get_product_rating(product, site=site)
    
    if rating is not None:
        rating = "%0.1f" % rating
        if rating.endswith('.0'):
            rating = rating[0]
        rating = rating + "/5"
    else:
        rating = _('Not Rated')
        
    return rating
    
