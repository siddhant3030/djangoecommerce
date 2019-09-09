from django import forms
from django.utils.safestring import mark_safe
from l10n.l10n_settings import get_l10n_default_currency_symbol
from satchmo_utils.numbers import round_decimal
import logging
from django.utils.html import escape
from decimal import Decimal

log = logging.getLogger('satchmo_utils.widgets')

def _render_decimal(value, places=2, min_places=2):
    # Check to make sure this is a Decimal before we try to round
    # and format. If it's not, just pass it on.
    # The admin validation will handle making sure only valid values get
    # saved.
    bad_decimal = False
    try:
        decimal_value = Decimal(value)
    except:
        bad_decimal = True
    if value is not None and not bad_decimal:
        roundfactor = "0." + "0"*(places-1) + "1"
        if decimal_value < 0:
            roundfactor = "-" + roundfactor

        value = round_decimal(val=value, places=places, roundfactor=roundfactor, normalize=True)
        log.debug('value: %s' % type(value))
        parts = ("%f" % value).split('.')
        n = parts[0]
        d = ""

        if len(parts) > 0:
            d = parts[1]
        elif min_places:
            d = "0" * min_places

        while len(d) < min_places:
            d = "%s0" % d

        while len(d) > min_places and d[-1] == '0':
            d = d[:-1]

        if len(d) > 0:
            value = "%s.%s" % (n, d)
        else:
            value = n
    return value

class BaseCurrencyWidget(forms.TextInput):
    """
    A Text Input widget that shows the currency amount
    """
    def __init__(self, attrs={}):
        final_attrs = {'class': 'vCurrencyField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(BaseCurrencyWidget, self).__init__(attrs=final_attrs)

class CurrencyWidget(BaseCurrencyWidget):

    def render(self, name, value, **kwargs):
        if value != '':
            value = _render_decimal(value, places=8)
        rendered = super(CurrencyWidget, self).render(name, value, **kwargs)
        curr = get_l10n_default_currency_symbol()
        curr = curr.replace("_", "&nbsp;")
        return mark_safe('<span class="currency">%s</span>%s' % (curr, rendered))

class TruncatedCurrencyWidget(BaseCurrencyWidget):
    """
    A Text Input widget that shows the currency amount - stripped to two digits by default.
    """

    def render(self, name, value, **kwargs):
        value = _render_decimal(value, places=2)
        rendered = super(TruncatedCurrencyWidget, self).render(name, value, **kwargs)
        curr = get_l10n_default_currency_symbol()
        curr = curr.replace("_", "&nbsp;")
        return mark_safe('<span class="currency">%s</span>%s' % (curr, rendered))

class StrippedDecimalWidget(forms.TextInput):
    """
    A textinput widget that strips out the trailing zeroes.
    """

    def __init__(self, attrs={}):
        final_attrs = {'class': 'vDecimalField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(StrippedDecimalWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value,  **kwargs):
        value = _render_decimal(value, places=8, min_places=0)
        return super(StrippedDecimalWidget, self).render(name, value, **kwargs)


