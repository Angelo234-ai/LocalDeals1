from django.contrib.admin.decorators import register

from Users.models import Profile
from .models import Category
from django.contrib.auth.models import User


def Products_and_Users(request):
    return {
        'Category_list': Category.objects.all(),
        'search_query': request.GET.get("search_query"),
        'featured': request.GET.get("featured"),


    }
