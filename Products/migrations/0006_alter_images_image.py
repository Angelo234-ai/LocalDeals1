# Generated by Django 3.2.6 on 2021-11-19 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_alter_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, default='products/default-image.jpg', null=True, upload_to='users/products-images', verbose_name='Images'),
        ),
    ]
