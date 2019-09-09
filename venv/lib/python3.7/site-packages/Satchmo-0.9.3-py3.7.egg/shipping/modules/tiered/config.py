from django.utils.translation import ugettext_lazy as _

from livesettings.values import ConfigurationGroup, StringValue
from livesettings.functions import config_register
import logging
log = logging.getLogger('tiered.config')
from shipping.config import SHIPPING_ACTIVE

SHIPPING_ACTIVE.add_choice(('shipping.modules.tiered', _('Tiered Shipping')))

log.debug('loaded')


SHIPPING_TIERED_GROUP = ConfigurationGroup('SHIPPING_TIERED', _('Shipping Tiered Settings'))

config_register(
    StringValue(SHIPPING_TIERED_GROUP,
        'MIN_PRICE_FOR',
        description = _("Min Price relates to"),
        help_text = _("By default Min Price only for total of shippable items"),
        default='SHIPPABLE',
        ordering=15,
        choices = (
            ('SHIPPABLE', _('Only shippable items')),
            ('NOT_DISCOUNTABLE', _('Not discountable total')),
        )))
