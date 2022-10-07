from django.forms.fields import ImageField
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Profile, Message

from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .utils import paginateProducts

from django.contrib import messages

from .forms import ReviewForm
from Products.models import Product


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "index")

        else:
            messages.error(request, "username or password is incorrect")

    return render(request, "users/login.html")


def LogoutUser(request):
    logout(request)
    messages.info(request, "Succesfully logged out")
    return redirect('login',)


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect("index")
        else:
            messages.success(
                request, "An error has occured during registration")

    context = {"form": form}
    return render(request, "users/register.html", context)


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('login')


class SingleProfile(FormMixin, DetailView):
    model = Profile
    template_name = "users/user-profile.html"
    context_object_name = 'profile'
    form_class = ReviewForm

    def get_object(self):
        return Profile.objects.get(id=self.kwargs.get("id"))


class SingleProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["username", "first_name", "last_name",
              "profile_image", "email", "location"]
    template_name = "users/user-profile-edit.html"

    def get_object(self):
        return Profile.objects.get(id=self.kwargs.get("id"))

    def form_valid(self, form):
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('user-dashboard', kwargs={"page": "all"}))


@login_required(login_url="login")
def AddFavProduct(request, id):
    product = get_object_or_404(Product, id=id)
    profile = request.user.profile.id
    if product.favourites.filter(id=profile):
        product.favourites.remove(profile)
    else:
        product.favourites.add(profile)
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(request.session['login_from'])


@login_required(login_url="login")
def ArchiveProduct(request, id, page):
    product = Product.objects.get(id=id)
    if page == "archive":
        product.archived = True
        product.in_stock = False
        product.is_active = False
        product.save()
    if page == "unarchive":
        product.archived = False
        product.in_stock = True
        product.is_active = True
        product.save()

    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(request.session['login_from'])


@login_required(login_url="login")
def UserDashboardView(request, page):
    profile = request.user.profile
    if page == "Favourite":
        products = profile.favourites.all()
    elif page == "Archived":
        products = profile.products.filter(
            archived=True, in_stock=False, is_active=False)
    elif page == "Pending Approval":
        products = profile.products.filter(in_stock=False, is_active=False)
    else:
        products = profile.products.filter(in_stock=True, is_active=True)

    archived_ads = profile.products.filter(
        archived=True, in_stock=False, is_active=False)

    page_obj = paginateProducts(request, products, 5)

    context = {
        "page_obj": page_obj,
        "profile": profile,
        "page": page,
        "archived_ads": archived_ads
    }

    return render(request, "users/dashboard/dashboard.html", context)


class CreateMessageView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Message
    fields = [
        'name',
        'email',
        'subject',
        'body',
    ]
    template_name = "users/create-message.html"

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        user = self.request.user.profile
        recipient = Profile.objects.get(id=self.kwargs.get('id'))
        obj.sender = user
        obj.recipient = recipient
        obj.save()
        return redirect(self.request.GET["next"] if "next" in self.request.GET else "index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(id=self.kwargs.get('id'))
        return context


class UserInboxView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "users/inbox.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        Messages = profile.messages.all()
        page = self.kwargs.get("page")
        if page == "Inbox":
            messages = Messages.filter(stared=False, trash=False)
        if page == "Stared":
            messages = Messages.filter(stared=True)
        elif page == "Sent":
            messages = Message.objects.filter(sender=profile.id,)
        elif page == "Trash":
            messages = Messages.filter(trash=True)

        page_obj = paginateProducts(self.request, messages, 10)
        context = {
            "pages": ["Inbox", "Stared", "Sent", "Trash"],
            "current_page": page,
            "profile": profile,
            "page_obj": page_obj
        }
        return context


class MessageView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = Message
    template_name = "users/open-message.html"
    context_object_name = 'message'

    def get_object(self):
        return Message.objects.get(id=self.kwargs.get("id"))


class ReplyMessageView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Message
    fields = [
        'subject',
        'body',
    ]
    template_name = "users/reply-message.html"

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        user = self.request.user.profile
        recipient = Profile.objects.get(id=self.kwargs.get('id'))
        obj.sender = user
        obj.recipient = recipient
        obj.save()
        return redirect(self.request.GET["next"] if "next" in self.request.GET else "index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(id=self.kwargs.get('id'))
        return context


@login_required(login_url="login")
def AddStaredMessage(request, id):
    message = get_object_or_404(Message, id=id)
    if message.stared == False:
        message.stared = True
    else:
        message.stared = False
    message.save()
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(request.session['login_from'])


@login_required(login_url="login")
def TrashMessage(request, id):
    message = get_object_or_404(Message, id=id)
    if message.trash == False:
        message.trash = True
    else:
        message.trash = False
    message.save()
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(request.session['login_from'])
