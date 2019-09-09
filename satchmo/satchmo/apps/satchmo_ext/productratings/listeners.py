"""Utility functions used by signals to attach Ratings to Comments"""
import logging

from django.contrib.sites.models import Site
from django.utils.encoding import smart_str
from django.conf import settings
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
try:
    from django.contrib.comments.models import Comment
except ImportError:
    from django_comments.models import Comment

from livesettings.functions import config_value
from product.models import Product
from satchmo_utils import url_join
from .models import ProductRating


log = logging.getLogger('productratings')

def save_rating(comment=None, request=None, **kwargs):
    """Create a rating and save with the comment"""
    
    # should always be true
    if request.method != "POST":
        return
    
    data = request.POST.copy()
    if 'rating' not in data:
        return
    
    raw = data['rating']
    try:
        rating = int(raw)
    except ValueError:
        log.error('Could not parse rating from posted rating: %s', raw)
        return
        
    if comment.content_type.app_label == "product" and comment.content_type.model == "product":
        ProductRating.objects.update_or_create(comment=comment, defaults = {'rating': rating})
    else:
        log.debug('Not saving rating for comment on a %s object', comment.content_type.model)
    
def one_rating_per_product(comment=None, request=None, **kwargs):
    site = Site.objects.get_current()
    product_ratings = ProductRating.objects.rated_products()
    product_ratings = product_ratings.filter(comment__object_pk=comment.object_pk, comment__site=site,
                                             comment__user=request.user).exclude(comment__pk=comment.pk).distinct()
                               
    for product_rating in product_ratings:
        product_rating.comment.delete()            

def check_with_akismet(comment=None, request=None, **kwargs):
    if config_value("PRODUCT", "AKISMET_ENABLE"):
        akismet_key = config_value("PRODUCT", "AKISMET_KEY")
        if akismet_key:             
            site = Site.objects.get_current()
            shop = reverse('satchmo_shop_home')
            from akismet import Akismet
            akismet = Akismet(
                key=akismet_key,
                blog_url='http://%s' % url_join(site.domain, shop))
            if akismet.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referrer': request.META.get('HTTP_REFERER', ""),
                                 'user_ip': comment.ip_address,
                                 'user_agent': '' }
                if akismet.comment_check(smart_str(comment.comment), data=akismet_data, build_data=True):
                    comment.is_public=False
                    comment.save()
                    log.info("Akismet marked comment #%i as spam", comment.id)
                else:
                    log.debug("Akismet accepted comment #%i", comment.id)
            else:
                log.warn("Akismet key '%s' not accepted by akismet service.", akismet_key)
        else:
            log.info("Akismet enabled, but no key found.  Please put in your admin settings.")
