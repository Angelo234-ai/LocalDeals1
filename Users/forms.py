from Products.models import Review
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email",
                  "username", "password1", "password2"]
        labels = {"first_name": "Name", }

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({"class": "border p-3 w-100 my-2"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "body"]
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment',
        }
