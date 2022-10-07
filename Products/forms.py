from django import forms
from .models import Product, Images, Review, Category, SubCategory


class ProductForm(forms.ModelForm):
    

    class Meta:
        model = Product
        fields = ("category",
                  "subcategory",
                  "Product_name",
                  "Short_des",
                  "Description",
                  "Manufacturer",
                  "model",
                  "price",
                  "condition",
                  "city",)
        
        
    def __init__(self, *args, **kwargs): 
        category = kwargs.pop("category", None)
        print(category)

        queryset = SubCategory.objects.all()
        if category:
            #queryset = SubCategory.objects.filter(category=category)
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            

        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['subcategory'].queryset =  queryset
        
        #self.fields['subcategory'].queryset = queryset
            
        

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image', )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("body", "rating")
        
        

