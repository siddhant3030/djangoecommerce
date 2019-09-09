from livesettings.functions import config_register_list
from livesettings.values import ConfigurationGroup, BooleanValue, ModuleValue, StringValue, MultipleStringValue
from django.utils.translation import ugettext_lazy as _

# this is so that the translation utility will pick up the string
gettext = lambda s: s
_strings = (gettext('CreditCard'), gettext('Credit Card'))

PAYMENT_GROUP = ConfigurationGroup('PAYMENT_PAYFLOWPRO',
    _('PayflowPro Payment Settings'),
    ordering=101)

config_register_list(

    BooleanValue(PAYMENT_GROUP,
        'LIVE',
        description=_("Accept real payments"),
        help_text=_("False if you want to submit to the test urls.  NOTE: Look "
                    "at the PayflowPro developer's guide "
                    "(https://cms.paypal.com/us/cgi-bin/?cmd=_render-content"
                    "&content_ID=developer/howto_gateway_payflowpro) for the "
                    "list of valid credit card numbers."),
        default=False),

    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description=_('Implementation module'),
        hidden=True,
        default = 'payment.modules.payflowpro'),

    BooleanValue(PAYMENT_GROUP,
        'CAPTURE',
        description=_('Capture Payment immediately?'),
        default=True,
        help_text=_('IMPORTANT: If false, a capture attempt will be '
                    'made when the order is marked as shipped.')),

    StringValue(PAYMENT_GROUP,
        'KEY',
        description=_("Module key"),
        hidden=True,
        default = 'PAYFLOWPRO'),

    StringValue(PAYMENT_GROUP,
        'LABEL',
        description=_('English name for this group on the checkout screens'),
        default = 'Credit Cards',
        dummy = _('Credit Cards'), # Force this to appear on po-files
        help_text = _('This will be passed to the translation utility')),

    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description=_('The url base used for constructing urlpatterns which '
                      'will use this module'),
        default = r'^credit/'),

    MultipleStringValue(
        PAYMENT_GROUP,
        'CREDITCHOICES',
        description=_('Available credit cards'),
        choices = (
            (('American Express', 'American Express')),
            (('Visa','Visa')),
            (('Mastercard','Mastercard')),
            (('Discover','Discover')),
            (('Diners Club', 'Diners Club')),
            (('JCB', 'JCB')),
            ),
        default = ('Visa', 'Mastercard')),
    
    StringValue(PAYMENT_GROUP,
        'PARTNER',
        description=_("Your authorized PayPal reseller's id."),
        default="PayPal"),

    StringValue(PAYMENT_GROUP,
        'VENDOR',
        description=_("Your merchant login ID that you created when you "
                      "registered for the account."),
        default="VENDOR_ID"),

    StringValue(PAYMENT_GROUP,
        'USER',
        description=_("If you set up more additional users on the PayPal "
                      "account, this value is the ID of the user authorized to "
                      "process transactions. If you have not set up additional "
                      "users on the account, has the same value as VENDOR."),
        default="VENDOR_ID"),

    StringValue(
        PAYMENT_GROUP,
        'PASSWORD',
        description=_("Your PayflowPro account password"),
        default=""),

    #BooleanValue(PAYMENT_GROUP,
        #'CAPTURE',
        #description=_('Capture Payment immediately?'),
        #default=True,
        #help_text=_('IMPORTANT: If false, a capture attempt will be made when '
        #            'the order is marked as shipped.')),

    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description=_("Verbose logs"),
        help_text=_("Add extensive logs during post."),
        default=False)
    )
