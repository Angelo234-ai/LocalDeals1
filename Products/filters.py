import django
from django.db.models import Q, fields, query
from django import forms
from django.db.models.deletion import PROTECT
from django.db.models.query_utils import subclasses
from django.forms.widgets import Select
from django.utils.regex_helper import contains
from django_filters import widgets
from django_filters.filters import ModelChoiceFilter
from .models import Product, Category, SubCategory
import django_filters
from django_filters.widgets import RangeWidget

options = (
    ("Brand_new", "Brand New"),
    ("like_new", "Like New"),
    ("Used", "Used"),
    ("very_used", "Very New"),
    ("fair", "Fair Condition"),
)


class ProductFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control my-2 my-lg-0', 'id': "inputtext4", 'placeholder': 'What are you looking for'}),
                                  method='my_custom_filter',
                                  label="Search")
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control my-2 my-lg-0', 'id': "inputtext4", 'placeholder': 'City'}),
                                     method='City_filter',
                                     label="City")
    Manufacturer = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control my-2 my-lg-0', 'id': "inputtext4", 'placeholder': 'Manufacturer'}),
                                             method='Manufacturer_filter',
                                             label="Manufacturer")
    model = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control my-2 my-lg-0', 'id': "inputtext4", 'placeholder': 'Model'}),
                                      method='Model_filter',
                                      label="Model")

    category = django_filters.ModelChoiceFilter(empty_label="Category",  queryset=Category.objects.all(),
                                                widget=forms.Select(
                                                    attrs={'class': "w-100 form-control mt-lg-1 mt-md-2", 'id': "inputCategory4"}),
                                                )
    subcategory = django_filters.ModelMultipleChoiceFilter(
        widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'this.form.submit()', 'class': 'checkbox'},))

    condition = django_filters.MultipleChoiceFilter(choices=options,
                                                    widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'this.form.submit()'}))

    price = django_filters.NumericRangeFilter()

    lowest = django_filters.OrderingFilter(choices=(
        ('price', 'low to high'), ('-price', 'high to low')),
    )

    class Meta:
        model = Product
        fields = {
            'category': ['in'],
            'condition': ['icontains', ],
            'price': ['contains'],
            'city': ['icontains', ],
            'subcategory': ['in', ],
            'Manufacturer': ['icontains', ],
            'model': ['icontains', ],

        }

    def my_custom_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(Product_name__icontains=value) |
            Q(Short_des__icontains=value) |
            Q(Description__icontains=value) |
            Q(Manufacturer__icontains=value) |
            Q(model__icontains=value)
        )

    def City_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(city__icontains=value)
        )

    def Manufacturer_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(Manufacturer__icontains=value)
        )

    def Model_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(model__icontains=value)
        )

    def Low_to_highFilter(self, queryset, name, value):
        return Product.objects.order_by("-price")

    def __init__(self, *args, **kwargs, ):
        super(ProductFilter, self).__init__(*args, **kwargs)

        # First Method
        category_input = args[0].get("category")
        subcategory_input = args[0].get("subcategory")

        if category_input:
            category = Category.objects.all()[int(category_input)-1]
            self.filters['subcategory'].extra.update({
                'queryset': SubCategory.objects.filter(Category=category.id),
            })

        else:
            self.filters['subcategory'].extra.update({
                'queryset': SubCategory.objects.all()
            })

        if subcategory_input:
            category = Category.objects.get(subcat=subcategory_input)
            self.filters['subcategory'].extra.update({
                'queryset': SubCategory.objects.filter(Category=category.id)
            })

            for name, field in self.filters.items():
                if isinstance(field, ModelChoiceFilter):
                    field.extra['empty_label'] = category

        else:
            self.filters['category'].extra.update({
                'queryset': Category.objects.all()
            })
