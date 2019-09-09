from django.contrib import admin

from payment.models import CreditCardDetail
from payment.forms import CreditCardDetailAdminForm


class CreditCardDetail_Inline(admin.StackedInline):
    model = CreditCardDetail
    form = CreditCardDetailAdminForm
    extra = 1


