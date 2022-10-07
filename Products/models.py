from django.contrib.admin.decorators import register
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
import uuid
from django.utils.regex_helper import Choice, flatten_result
from Users.models import Profile


from Users.models import Profile


class Category(models.Model):
    Name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.Name


class SubCategory(models.Model):
    Name = models.CharField(max_length=200)
    Category = models.ForeignKey(
        Category, related_name="subcat", on_delete=Model.delete)

    class Meta:
        ordering = ["Category", ]

    def __str__(self):
        return f"{self.Name}"


class Product(models.Model):
    options = (
        ("Brand_new", "Brand New"),
        ("like_new", "Like New"),
        ("Used", "Used"),
        ("very_used", "Very New"),
        ("fair", "Fair Condition"),
    )
    Owner = ForeignKey(Profile, on_delete=models.CASCADE, default=1,
                       blank=True, null=True, related_name="products")
    category = ForeignKey(
        Category, blank=True, default=None, on_delete=models.CASCADE, related_name='subcategories')
    subcategory = models.ForeignKey(
        SubCategory, related_name="product", on_delete=models.CASCADE)
    Product_name = models.CharField(max_length=50, null=True, blank=True)
    Short_des = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Manufacturer = models.CharField(
        max_length=50, null=True, blank=True, default='-')
    model = models.CharField(max_length=50, null=True,
                             blank=True, default='-')
    price = models.IntegerField()
    condition = models.CharField(
        choices=options, max_length=50, null=True, blank=True)
    favourites = ManyToManyField(
        Profile, related_name="favourites", default=None, blank=True)
    archived = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    city = models.CharField(max_length=50, default="Your City")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.Product_name

    @ property
    def reviewers(self):
        queryset = self.review.all().values_list("owner__id", flat=True)
        return queryset

    @ property
    def getVoteCount(self):
        reviews = self.review.all()
        Totalvotes = reviews.count()
        rating_1 = reviews.filter(rating="⭐").count()
        rating_2 = reviews.filter(rating="⭐⭐").count()
        rating_3 = reviews.filter(rating="⭐⭐⭐").count()
        rating_4 = reviews.filter(rating="⭐⭐⭐⭐").count()
        rating_5 = reviews.filter(rating="⭐⭐⭐⭐⭐").count()

        ratio = 1*rating_1 + 2*rating_2 + 3*rating_3 + \
            4*rating_4 + 5*rating_5 / Totalvotes

        self.vote_total = Totalvotes
        self.vote_ratio = round(ratio)
        self.save()


class Images(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="Images", )
    image = models.ImageField(upload_to="users/products-images",
                              verbose_name='Images', null=True, blank=True, default="image")


class Review(models.Model):
    rating_choices = (
        ("⭐", "⭐"),
        ("⭐⭐", "⭐⭐"),
        ("⭐⭐⭐", "⭐⭐⭐"),
        ("⭐⭐⭐⭐", "⭐⭐⭐⭐"),
        ("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"),
    )

    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="review")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review")
    body = models.TextField(max_length=500)
    rating = models.CharField(
        max_length=5, choices=rating_choices, default="⭐⭐⭐⭐⭐")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [["owner", "product"]]

    def __str__(self):
        return str(self.product.Product_name)
