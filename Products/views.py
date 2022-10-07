from django.forms.fields import NullBooleanField
from django.http import request
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, FormView
from Products import forms
from django.http.response import HttpResponseRedirect

from Users.forms import ReviewForm
from .filters import ProductFilter
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Product, Images
from django.contrib.auth.models import User

from .filters import ProductFilter
from . import forms
from django.forms import modelformset_factory


class ProductListView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        Product_list = super().get_queryset(**kwargs)
        context.update({
            'filter': ProductFilter(
                self.request.GET, queryset=Product_list),
        })

        return context


class ProductSearch(ListView):
    model = Product
    template_name = "products/ad-list-view.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data(**kwargs)
        Product_list = super().get_queryset(**kwargs)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()

        context.update({
            'filter': ProductFilter(
                self.request.GET, queryset=Product_list),
            'parameters': parameters
        })

        return context

    def get_queryset(self):
        Product_list = super().get_queryset()

        return ProductFilter(self.request.GET, queryset=Product_list).qs

        # evaluate if the checkbox is checked


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/single.html"
    context_object_name = 'product'

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get("id"))
        if product.vote_ratio != 0:
            product.getVoteCount

        context['form'] = forms.ReviewForm
        context['filter_form'] = ProductFilter(
            self.request.GET, )
        context['vote_ratio'] = range(product.vote_ratio)
        return context


@login_required(login_url="login")
def ReviewFormView(request, id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.product = Product.objects.get(id=id)
        review.save()
        return redirect(request.GET["next"] if "next" in request.GET else "index")


class CreateProductView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Product
    form_class = forms.ProductForm
    template_name = "products/product-create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        context['page'] = "Create listing"
        ImageFormSet = modelformset_factory(Images,
                                            form=forms.ImageForm, extra=3)
        context['ImageForm'] = ImageFormSet(queryset=Images.objects.none(),)
        context['form'] = forms.ProductForm()
        return context

    def form_valid(self, form):
        ImageFormSet = modelformset_factory(Images,
                                            form=forms.ImageForm, extra=3)
        images_form = ImageFormSet(self.request.POST, self.request.FILES,
                                   queryset=Images.objects.none())

        if images_form.is_valid() and form.is_valid():
            obj = form.save(commit=False)
            obj.Owner = self.request.user.profile
            obj.save()

            for form in images_form.cleaned_data:
                if form != {}:
                    image = form['image']
                    photo = Images(product=obj, image=image)
                    photo.save()

        return HttpResponseRedirect(reverse('user-dashboard', kwargs={"page": "all"}))
    

    
    
def load_Subcategories(request):
        category_id = request.GET.get('category')
        subcategories = Subcategory.objects.filter(category_id=category_id)
        return render(request, 'products/subcategory_dropdown_list_options.html', {'subcategories': subcategories})
    


class EditProductView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = Product
    form_class = forms.ProductForm
    template_name = "products/product-edit.html"

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))

    def form_valid(self, form):
        ImageFormSet = modelformset_factory(Images,
                                            form=forms.ImageForm, extra=3)
        product = Product.objects.get(id=self.kwargs.get("id"))
        qs = Images.objects.filter(product=product)
        images_form = ImageFormSet(self.request.POST, self.request.FILES,
                                   queryset=qs)
        product_form = form.save(commit=False)

        if form.is_valid() and images_form.is_valid():
            product_form.save()
            obj = form.save(commit=False)
            obj.Owner = self.request.user.profile
            form.save()
            for image in images_form.cleaned_data:
                if image != {}:
                    image = image['image']
                    photo = Images(product=obj, image=image)

                    photo.save()

        return HttpResponseRedirect(reverse('user-dashboard', kwargs={"page": "all"}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get("id"))
        qs = Images.objects.filter(product=product)
        ImageFormSet = modelformset_factory(Images,
                                            form=forms.ImageForm, extra=0)

        if len(ImageFormSet(queryset=qs)) != 3:
            extra = 0
            product_images_count = len(ImageFormSet(queryset=qs))
            while product_images_count != 3:
                extra += 1
                product_images_count += 1
        else:
            extra = 0

        ImageFormSet = modelformset_factory(Images,
                                            form=forms.ImageForm, extra=extra)
        context['ImageForm'] = ImageFormSet(queryset=qs)

        context['page'] = "Edit"
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = Product

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))

    def get_success_url(self):
        return redirect(request.GET["next"] if "next" in request.GET else "index")


def error_404(request, exception):
    return render(request, '404.html')
