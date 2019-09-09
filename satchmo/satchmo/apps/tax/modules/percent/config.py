from django.utils.translation import ugettext_lazy as _
from livesettings.values import BooleanValue,DecimalValue
from livesettings.functions import config_register,config_get_group
from tax.config import TAX_MODULE

TAX_MODULE.add_choice(('tax.modules.percent', _('Percent Tax')))
TAX_GROUP = config_get_group('TAX')

config_register(
    DecimalValue(TAX_GROUP,
        'PERCENT',
        description=_("Percent tax"),
        requires=TAX_MODULE,
        requiresvalue='tax.modules.percent',
        default="0")
)

config_register(
    BooleanValue(TAX_GROUP,
        'TAX_SHIPPING_PERCENT',
        description=_("Tax Shipping?"),
        requires=TAX_MODULE,
        requiresvalue='tax.modules.percent',
        default=False)
)
