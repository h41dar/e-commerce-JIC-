# Generated by Django 5.1 on 2024-09-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]