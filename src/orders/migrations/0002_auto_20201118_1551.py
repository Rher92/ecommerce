# Generated by Django 3.1.3 on 2020-11-18 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='cuantity',
            new_name='quantity',
        ),
    ]