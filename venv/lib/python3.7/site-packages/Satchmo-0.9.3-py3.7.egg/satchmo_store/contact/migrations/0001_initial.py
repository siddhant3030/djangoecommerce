# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('l10n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(help_text='Description of address - Home, Office, Warehouse, etc.', max_length=20, verbose_name='Description', blank=True)),
                ('addressee', models.CharField(max_length=80, verbose_name='Addressee')),
                ('street1', models.CharField(max_length=80, verbose_name='Street')),
                ('street2', models.CharField(max_length=80, verbose_name='Street', blank=True)),
                ('state', models.CharField(max_length=50, verbose_name='State', blank=True)),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('postal_code', models.CharField(max_length=30, verbose_name='Zip Code')),
                ('is_default_shipping', models.BooleanField(default=False, verbose_name='Default Shipping Address')),
                ('is_default_billing', models.BooleanField(default=False, verbose_name='Default Billing Address')),
            ],
            options={
                'verbose_name': 'Address Book',
                'verbose_name_plural': 'Address Books',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='Title', blank=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last name')),
                ('dob', models.DateField(null=True, verbose_name='Date of birth', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Email', blank=True)),
                ('notes', models.TextField(max_length=500, verbose_name='Notes', blank=True)),
                ('create_date', models.DateField(verbose_name='Creation date')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactInteractionType',
            fields=[
                ('key', models.CharField(max_length=30, unique=True, serialize=False, verbose_name='Key', primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactOrganization',
            fields=[
                ('key', models.CharField(max_length=30, unique=True, serialize=False, verbose_name='Key', primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Contact organization type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactOrganizationRole',
            fields=[
                ('key', models.CharField(max_length=30, unique=True, serialize=False, verbose_name='Key', primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactRole',
            fields=[
                ('key', models.CharField(max_length=30, unique=True, serialize=False, verbose_name='Key', primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField(verbose_name='Date and Time')),
                ('description', models.TextField(max_length=200, verbose_name='Description')),
                ('contact', models.ForeignKey(verbose_name='Contact', to='contact.Contact', on_delete=models.CASCADE)),
                ('type', models.ForeignKey(verbose_name='Type', to='contact.ContactInteractionType', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Interaction',
                'verbose_name_plural': 'Interactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('create_date', models.DateField(verbose_name='Creation Date')),
                ('notes', models.TextField(max_length=200, null=True, verbose_name='Notes', blank=True)),
                ('role', models.ForeignKey(verbose_name='Role', to='contact.ContactOrganizationRole', null=True, on_delete=models.SET_NULL)),
                ('type', models.ForeignKey(verbose_name='Type', to='contact.ContactOrganization', null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(blank=True, max_length=20, verbose_name='Description', choices=[('Work', 'Work'), ('Home', 'Home'), ('Fax', 'Fax'), ('Mobile', 'Mobile')])),
                ('phone', models.CharField(max_length=30, verbose_name='Phone Number', blank=True)),
                ('primary', models.BooleanField(default=False, verbose_name='Primary')),
                ('contact', models.ForeignKey(to='contact.Contact', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-primary'],
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(verbose_name='Organization', blank=True, to='contact.Organization', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.ForeignKey(verbose_name='Role', to='contact.ContactRole', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addressbook',
            name='contact',
            field=models.ForeignKey(to='contact.Contact', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addressbook',
            name='country',
            field=models.ForeignKey(verbose_name='Country', to='l10n.Country', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
