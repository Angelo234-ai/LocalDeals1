# Generated by Django 3.2.6 on 2021-11-18 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_alter_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/products-images', verbose_name='Images'),
        ),
        migrations.AlterField(
            model_name='images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='Products.product'),
        ),
    ]
