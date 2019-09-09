from satchmo_store.shop.signals import satchmo_cart_add_complete
from .views import cart_add_listener

satchmo_cart_add_complete.connect(cart_add_listener, sender=None)
