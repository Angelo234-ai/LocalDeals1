from django.urls import path
from Products.forms import ReviewForm
from Products.views import ProductDeleteView, ProductDetailView, ProductListView, ProductSearch, CreateProductView, EditProductView, ReviewFormView, load_Subcategories

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product-search",
         ProductSearch.as_view(), name="Product-search"),
    path("Product-detail/<id>",
         ProductDetailView.as_view(), name="Product-detail"),
    path("Product-delete/<id>",
         ProductDeleteView.as_view(), name="Product-delete"),
    path("Product-Create",
         CreateProductView.as_view(), name="Create-product"),
    path("Product-edit/<id>",
         EditProductView.as_view(), name="Edit-product"),
    path("ReivewForm/<id>",
         ReviewFormView, name="review"),
    path('ajax/load-subcatgories/', load_Subcategories, name='ajax_load_subcatgories'),  # <-- this one here

]
