# Generated by Django 5.1 on 2024-09-12 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_itemstatus_delete_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemstatus',
            name='added_at',
        ),
    ]
