from django.contrib.auth.models import User
from django.urls import path
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from .views import AuthorDeleteView, SingleProfile, SingleProfileEdit, UserDashboardView, UserInboxView, CreateMessageView, AddFavProduct, UserInboxView, loginUser, LogoutUser, registerUser, ArchiveProduct
from Users import views

urlpatterns = [
    path("login", loginUser, name="login"),
    path("logout", LogoutUser, name="logout"),
    path("register", registerUser, name="register"),
    path("<pk>/delete-user", AuthorDeleteView.as_view(), name="delete-user"),
    path("<id>", SingleProfile.as_view(), name="user-profile"),
    path("edit/<id>", SingleProfileEdit.as_view(), name="user-profile-edit"),
    path("dashboard/<str:page>",
         UserDashboardView, name="user-dashboard"),
    path("AddFavouriteProduct/<id>", AddFavProduct, name="fav-product"),
    path("ArchiveProduct/<id>/<page>", ArchiveProduct, name="archive-product"),

    path("user-inbox/<str:page>",
         UserInboxView.as_view(), name="user-inbox"),
    path("Send-message/<str:id>",
         CreateMessageView.as_view(), name="create-message"),
    path("open-message/<str:id>",
         views.MessageView.as_view(), name="open-message"),
    path("reply-message/<str:id>",
         views.ReplyMessageView.as_view(), name="reply-form"),
    path("trash-message/<str:id>",
         views.TrashMessage, name="trash-message"),
    path("star-message/<str:id>",
         views.AddStaredMessage, name="star-message"),
]
