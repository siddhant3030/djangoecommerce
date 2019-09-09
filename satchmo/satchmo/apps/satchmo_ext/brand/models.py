from __future__ import unicode_literals
import logging

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from l10n.mixins import TranslatedObjectMixin
import product
from product.models import Product
from satchmo_utils.satchmo_thumbnail.field import ImageWithThumbnailField
from satchmo_utils.signals import collect_urls


log = logging.getLogger('brand.models')

class BrandManager(models.Manager):
    
    def active(self, site=None):
        if not site:
            site = Site.objects.get_current()
        return self.filter(site=site, active=True)
    
    def by_slug(self, slug):
        site = Site.objects.get_current()
        return self.get(slug=slug, site=site)


@python_2_unicode_compatible
class Brand(models.Model, TranslatedObjectMixin):
    """A product brand"""
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"), unique=True,
    help_text=_("Used for URLs"))
    products = models.ManyToManyField(Product, blank=True, verbose_name=_("Products"), through='BrandProduct')
    ordering = models.IntegerField(_("Ordering"))
    active = models.BooleanField(default=True)
    
    objects = BrandManager()
    
    class Meta:
        ordering=('ordering', 'slug')
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
    
    def __str__(self):
        return "%s" % self.slug    
    
    @cached_property
    def active_categories(self):
        return [cat for cat in self.categories.all() if cat.has_content()]
    
    @cached_property
    def translation(self):
        return self._find_translation()

    def get_absolute_url(self):
        return reverse('satchmo_brand_view', kwargs={'brandname' : self.slug})
        
    def active_products(self):
        return self.products.filter(site=self.site, active=True)        

    def has_categories(self):
        return self.active_categories

    def has_content(self):
        return self.has_products() or self.has_categories()

    def has_products(self):
        return self.active_products().exists()
        

class BrandProduct(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name=_("Brand Product")
        verbose_name_plural=_("Brand Products")


class BrandTranslation(models.Model):
    brand = models.ForeignKey(Brand, related_name="translations", on_delete=models.CASCADE)
    languagecode = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES)
    name = models.CharField(_('title'), max_length=100, blank=False)
    short_description = models.CharField(_('Short Description'), blank=True, max_length=200)
    description = models.TextField(_('Full Description'), blank=True)
    picture = ImageWithThumbnailField(verbose_name=_('Picture'),
        upload_to="__DYNAMIC__",
        name_field="_filename",
        null=True, blank=True,
        max_length=200) #Media root is automatically prepended
    
    class Meta:
        ordering=('languagecode', )      
        verbose_name = _('Brand Translation')
        verbose_name_plural = _('Brand Translations')      
    
    @cached_property
    def _filename(self):
        if self.brand:
            return '%s-%s' % (self.brand.slug, self.id)
        else:
            return 'default'


class BrandCategoryManager(models.Manager):
    
    def by_slug(self, brandname, slug):
        brand = Brand.objects.by_slug(brandname)
        return brand.categories.get(slug=slug)


@python_2_unicode_compatible
class BrandCategory(models.Model, TranslatedObjectMixin):
    """A category within a brand"""
    slug = models.SlugField(_("Slug"), help_text=_("Used for URLs"))
    brand = models.ForeignKey(Brand, related_name="categories", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, verbose_name=_("Products"), through='BrandCategoryProduct')
    ordering = models.IntegerField(_("Ordering"))
    active = models.BooleanField(default=True)

    objects = BrandCategoryManager()

    class Meta:
        ordering=('ordering', 'slug')
        verbose_name = _('Brand Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return "%s: %s" % (self.brand.slug, self.slug)

    @cached_property
    def translation(self):
        return self._find_translation()

    def get_absolute_url(self):
        return reverse('satchmo_brand_category_view', kwargs={'brandname' : self.brand.slug, 'catname' : self.slug})
        
    def active_products(self):
        return self.products.filter(site=self.brand.site, active=True)                
        
    def has_categories(self):
        return False    
    
    def has_content(self):
        return self.active_products().exists()

    def has_products(self):
        return self.active_products().exists()


class BrandCategoryProduct(models.Model):
    brandcategory = models.ForeignKey(BrandCategory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('Brand Category Product')
        verbose_name_plural = _('Brand Category Products')


class BrandCategoryTranslation(models.Model):
    brandcategory = models.ForeignKey(BrandCategory, related_name="translations", on_delete=models.CASCADE)
    languagecode = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES)
    name = models.CharField(_('title'), max_length=100, blank=False)
    short_description = models.CharField(_('Short Description'), blank=True, max_length=200)
    description = models.TextField(_('Description'), blank=True)
    picture = ImageWithThumbnailField(verbose_name=_('Picture'),
        upload_to="__DYNAMIC__",
        name_field="_filename",
        null=True, blank=True,
        max_length=200) #Media root is automatically prepended
    
    class Meta:
        ordering=('languagecode', )
        verbose_name_plural = _('Brand Category Translations')    
    
    @cached_property
    def _filename(self):
        if self.brandcategory:
            return '%s-%s' % (self.brandcategory.brand.slug, self.id)
        else:
            return 'default'
    
    
from .urls import add_brand_urls
collect_urls.connect(add_brand_urls, sender=product)
