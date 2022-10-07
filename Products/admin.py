from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from .models import Product, Category, SubCategory, Review, Images
# Register your models here.


@admin.register(SubCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["Category", "Name"]
    list_filter = ["Category"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ["owner"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["category", "Owner", "subcategory", ]
    list_display = ["Product_name", "category", ]


@admin.register(Images)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["product", ]
    list_display = ["product", ]


admin.site.register(Category)
