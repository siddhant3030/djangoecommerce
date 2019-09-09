# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import satchmo_utils.fields
import product.models
import satchmo_utils.satchmo_thumbnail.field


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('name', models.SlugField(max_length=100, verbose_name='Attribute name')),
                ('validation', models.CharField(max_length=100, verbose_name='Field Validations', choices=[(b'product.utils.validation_simple', 'One or more characters'), (b'product.utils.validation_integer', 'Integer number'), (b'product.utils.validation_yesno', 'Yes or No'), (b'product.utils.validation_decimal', 'Decimal number')])),
                ('sort_order', models.IntegerField(default=1, verbose_name='Sort Order')),
                ('error_message', models.CharField(default='Invalid Entry', max_length=100, verbose_name='Error Message')),
            ],
            options={
                'ordering': ('sort_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(help_text='Used for URLs, auto-generated from name if blank', verbose_name='Slug', blank=True)),
                ('meta', models.TextField(help_text='Meta description for this category', null=True, verbose_name='Meta Description', blank=True)),
                ('description', models.TextField(help_text=b'Optional', verbose_name='Description', blank=True)),
                ('ordering', models.IntegerField(default=0, help_text='Override alphabetical order in category display', verbose_name='Ordering')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='product.Category', null=True, on_delete=models.SET_NULL)),
                ('related_categories', models.ManyToManyField(related_name='related_categories_rel_+', null=True, verbose_name='Related Categories', to='product.Category', blank=True)),
                ('site', models.ManyToManyField(to='sites.Site', verbose_name='Site')),
            ],
            options={
                'ordering': ['parent__ordering', 'parent__name', 'ordering', 'name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(blank=True, max_length=10, null=True, verbose_name='language', choices=[(b'en', b'English')])),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('category', models.ForeignKey(to='product.Category', on_delete=models.CASCADE)),
                ('option', models.ForeignKey(to='product.AttributeOption', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('option__sort_order',),
                'verbose_name': 'Category Attribute',
                'verbose_name_plural': 'Category Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', satchmo_utils.satchmo_thumbnail.field.ImageWithThumbnailField(max_length=200, upload_to=satchmo_utils.satchmo_thumbnail.field.upload_dir)),
                ('caption', models.CharField(max_length=100, null=True, verbose_name='Optional caption', blank=True)),
                ('sort', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('category', models.ForeignKey(related_name='images', blank=True, to='product.Category', null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'ordering': ['sort'],
                'verbose_name': 'Category Image',
                'verbose_name_plural': 'Category Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryImageTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('caption', models.CharField(max_length=255, verbose_name='Translated Caption')),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('categoryimage', models.ForeignKey(related_name='translations', to='product.CategoryImage', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('categoryimage', 'caption', 'languagecode'),
                'verbose_name': 'Category Image Translation',
                'verbose_name_plural': 'Category Image Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('name', models.CharField(max_length=255, verbose_name='Translated Category Name')),
                ('description', models.TextField(default=b'', verbose_name='Description of category', blank=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('category', models.ForeignKey(related_name='translations', to='product.Category', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('category', 'name', 'languagecode'),
                'verbose_name': 'Category Translation',
                'verbose_name_plural': 'Category Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('code', models.CharField(help_text='Coupon Code', unique=True, max_length=20, verbose_name='Discount Code')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('amount', satchmo_utils.fields.CurrencyField(decimal_places=2, max_digits=8, blank=True, help_text='Enter absolute discount amount OR percentage.', null=True, verbose_name='Discount Amount')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5, blank=True, help_text='Enter absolute discount amount OR percentage.  Percents are given in whole numbers, and can be up to 100%.', null=True, verbose_name='Discount Percentage')),
                ('automatic', models.NullBooleanField(default=False, help_text='Use this field to advertise the discount on all products to which it applies.  Generally this is used for site-wide sales.', verbose_name='Is this an automatic discount?')),
                ('allowedUses', models.IntegerField(help_text='Set this to a number greater than 0 to have the discount expire after that many uses.', null=True, verbose_name='Number of allowed uses', blank=True)),
                ('numUses', models.IntegerField(null=True, verbose_name='Number of times already used', blank=True)),
                ('minOrder', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Minimum order value', max_digits=8, decimal_places=2, blank=True)),
                ('startDate', models.DateField(verbose_name='Start Date')),
                ('endDate', models.DateField(verbose_name='End Date')),
                ('shipping', models.CharField(default=b'NONE', choices=[(b'NONE', 'None'), (b'FREE', 'Free Shipping'), (b'FREECHEAP', 'Cheapest shipping option is free'), (b'APPLY', 'Apply the discount above to shipping')], max_length=10, blank=True, null=True, verbose_name='Shipping')),
                ('allValid', models.BooleanField(default=False, help_text='Apply this discount to all discountable products? If this is false you must select products below in the "Valid Products" section.', verbose_name='All products?')),
                ('site', models.ManyToManyField(to='sites.Site', verbose_name='site')),
                ('valid_categories', models.ManyToManyField(to='product.Category', null=True, verbose_name='Valid Categories', blank=True)),
            ],
            options={
                'verbose_name': 'Discount',
                'verbose_name_plural': 'Discounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Display value')),
                ('value', models.CharField(max_length=50, verbose_name='Stored value')),
                ('price_change', satchmo_utils.fields.CurrencyField(decimal_places=6, max_digits=14, blank=True, help_text='This is the price differential for this option.', null=True, verbose_name='Price Change')),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
            ],
            options={
                'ordering': ('option_group', 'sort_order', 'name'),
                'verbose_name': 'Option Item',
                'verbose_name_plural': 'Option Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='This will be the text displayed on the product page.', max_length=50, verbose_name='Name of Option Group')),
                ('description', models.CharField(help_text='Further description of this group (i.e. shirt size vs shoe size).', max_length=100, verbose_name='Detailed Description', blank=True)),
                ('sort_order', models.IntegerField(default=0, help_text='The display order for this group.', verbose_name='Sort Order')),
                ('site', models.ManyToManyField(to='sites.Site', verbose_name='Site')),
            ],
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'Option Group',
                'verbose_name_plural': 'Option Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionGroupTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('name', models.CharField(max_length=255, verbose_name='Translated OptionGroup Name')),
                ('description', models.TextField(default=b'', verbose_name='Description of OptionGroup', blank=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('optiongroup', models.ForeignKey(related_name='translations', to='product.OptionGroup', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('optiongroup', 'name', 'languagecode'),
                'verbose_name': 'Option Group Translation',
                'verbose_name_plural': 'Option Groups Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('name', models.CharField(max_length=255, verbose_name='Translated Option Name')),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('option', models.ForeignKey(related_name='translations', to='product.Option', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('option', 'name', 'languagecode'),
                'verbose_name': 'Option Translation',
                'verbose_name_plural': 'Option Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', satchmo_utils.fields.CurrencyField(verbose_name='Price', max_digits=14, decimal_places=6)),
                ('quantity', models.DecimalField(default=b'1.0', help_text='Use this price only for this quantity or higher', verbose_name='Discount Quantity', max_digits=18, decimal_places=6)),
                ('expires', models.DateField(null=True, verbose_name='Expires', blank=True)),
            ],
            options={
                'ordering': ['expires', '-quantity'],
                'verbose_name': 'Price',
                'verbose_name_plural': 'Prices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='This is what the product will be called in the default site language.  To add non-default translations, use the Product Translation section below.', max_length=255, verbose_name='Full Name')),
                ('slug', models.SlugField(help_text='Used for URLs, auto-generated from name if blank', max_length=255, verbose_name='Slug Name', blank=True)),
                ('sku', models.CharField(help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='SKU', blank=True)),
                ('short_description', models.TextField(default=b'', help_text='This should be a 1 or 2 line description in the default site language for use in product listing screens', max_length=200, verbose_name='Short description of product', blank=True)),
                ('description', models.TextField(default=b'', help_text='This field can contain HTML and should be a few paragraphs in the default site language explaining the background of the product, and anything that would help the potential customer make their purchase.', verbose_name='Description of product', blank=True)),
                ('items_in_stock', models.DecimalField(default=b'0', verbose_name='Number in stock', max_digits=18, decimal_places=6)),
                ('meta', models.TextField(help_text='Meta description for this product', max_length=200, null=True, verbose_name='Meta Description', blank=True)),
                ('date_added', models.DateField(null=True, verbose_name='Date added', blank=True)),
                ('active', models.BooleanField(default=True, help_text='This will determine whether or not this product will appear on the site', verbose_name='Active')),
                ('featured', models.BooleanField(default=False, help_text='Featured items will show on the front page', verbose_name='Featured')),
                ('ordering', models.IntegerField(default=0, help_text='Override alphabetical order in category display', verbose_name='Ordering')),
                ('weight', models.DecimalField(null=True, verbose_name='Weight', max_digits=8, decimal_places=2, blank=True)),
                ('weight_units', models.CharField(max_length=3, null=True, verbose_name='Weight units', blank=True)),
                ('length', models.DecimalField(null=True, verbose_name='Length', max_digits=6, decimal_places=2, blank=True)),
                ('length_units', models.CharField(max_length=3, null=True, verbose_name='Length units', blank=True)),
                ('width', models.DecimalField(null=True, verbose_name='Width', max_digits=6, decimal_places=2, blank=True)),
                ('width_units', models.CharField(max_length=3, null=True, verbose_name='Width units', blank=True)),
                ('height', models.DecimalField(null=True, verbose_name='Height', max_digits=6, decimal_places=2, blank=True)),
                ('height_units', models.CharField(max_length=3, null=True, verbose_name='Height units', blank=True)),
                ('total_sold', models.DecimalField(default=b'0', verbose_name='Total sold', max_digits=18, decimal_places=6)),
                ('taxable', models.BooleanField(default=product.models.get_taxable, verbose_name='Taxable')),
                ('shipclass', models.CharField(default=b'DEFAULT', help_text="If this is 'Default', then we'll use the product type to determine if it is shippable.", max_length=10, verbose_name='Shipping', choices=[(b'DEFAULT', 'Default'), (b'YES', 'Shippable'), (b'NO', 'Not Shippable')])),
                ('also_purchased', models.ManyToManyField(related_name='also_purchased_rel_+', null=True, verbose_name='Previously Purchased', to='product.Product', blank=True)),
                ('category', models.ManyToManyField(to='product.Category', verbose_name='Category', blank=True)),
                ('related_items', models.ManyToManyField(related_name='related_items_rel_+', null=True, verbose_name='Related Items', to='product.Product', blank=True)),
                ('site', models.ManyToManyField(to='sites.Site', verbose_name='Site')),
            ],
            options={
                'ordering': ('ordering', 'name'),
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(blank=True, max_length=10, null=True, verbose_name='language', choices=[(b'en', b'English')])),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('option', models.ForeignKey(to='product.AttributeOption', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('option__sort_order',),
                'verbose_name': 'Product Attribute',
                'verbose_name_plural': 'Product Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', satchmo_utils.satchmo_thumbnail.field.ImageWithThumbnailField(max_length=200, upload_to=satchmo_utils.satchmo_thumbnail.field.upload_dir)),
                ('caption', models.CharField(max_length=100, null=True, verbose_name='Optional caption', blank=True)),
                ('sort', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('product', models.ForeignKey(blank=True, to='product.Product', null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'ordering': ['sort'],
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImageTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('caption', models.CharField(max_length=255, verbose_name='Translated Caption')),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('productimage', models.ForeignKey(related_name='translations', to='product.ProductImage', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('productimage', 'caption', 'languagecode'),
                'verbose_name': 'Product Image Translation',
                'verbose_name_plural': 'Product Image Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductPriceLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('siteid', models.IntegerField()),
                ('key', models.CharField(max_length=60, null=True)),
                ('parentid', models.IntegerField(null=True)),
                ('productslug', models.CharField(max_length=255, db_index=True)),
                ('price', models.DecimalField(max_digits=14, decimal_places=6)),
                ('quantity', models.DecimalField(max_digits=18, decimal_places=6)),
                ('active', models.BooleanField(default=False)),
                ('discountable', models.BooleanField(default=False)),
                ('items_in_stock', models.DecimalField(max_digits=18, decimal_places=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('description', models.TextField(default=b'', help_text='This field can contain HTML and should be a few paragraphs explaining the background of the product, and anything that would help the potential customer make their purchase.', verbose_name='Description of product', blank=True)),
                ('short_description', models.TextField(default=b'', help_text='This should be a 1 or 2 line description for use in product listing screens', max_length=200, verbose_name='Short description of product', blank=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('product', models.ForeignKey(related_name='translations', to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('product', 'name', 'languagecode'),
                'verbose_name': 'Product Translation',
                'verbose_name_plural': 'Product Translations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Displayed title of this tax.', max_length=20, verbose_name='Title')),
                ('description', models.CharField(help_text='Description of products that would be taxed.', max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Tax Class',
                'verbose_name_plural': 'Tax Classes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='producttranslation',
            unique_together=set([('product', 'languagecode', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='productimagetranslation',
            unique_together=set([('productimage', 'languagecode', 'version')]),
        ),
        migrations.AddField(
            model_name='product',
            name='taxClass',
            field=models.ForeignKey(blank=True, to='product.TaxClass', help_text='If it is taxable, what kind of tax?', null=True, verbose_name='Tax Class', on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(to='product.Product', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=set([('product', 'quantity', 'expires')]),
        ),
        migrations.AlterUniqueTogether(
            name='optiontranslation',
            unique_together=set([('option', 'languagecode', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='optiongrouptranslation',
            unique_together=set([('optiongroup', 'languagecode', 'version')]),
        ),
        migrations.AddField(
            model_name='option',
            name='option_group',
            field=models.ForeignKey(to='product.OptionGroup', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together=set([('option_group', 'value')]),
        ),
        migrations.AddField(
            model_name='discount',
            name='valid_products',
            field=models.ManyToManyField(to='product.Product', null=True, verbose_name='Valid Products', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('category', 'languagecode', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='categoryimagetranslation',
            unique_together=set([('categoryimage', 'languagecode', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='categoryimage',
            unique_together=set([('category', 'sort')]),
        ),
    ]
