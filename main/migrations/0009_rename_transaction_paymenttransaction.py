# Generated by Django 5.0.4 on 2025-04-02 20:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_property_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction',
            new_name='PaymentTransaction',
        ),
    ]
