from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from pydantic import ValidationError
from .models import Product

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Samuel Alarcón",
        })
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

#class Product:
 #   products = [
  #      {"id":"1", "name":"TV", "description":"Best TV", "price": 500},
   #     {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 300},
    #    {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 99},
     #   {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 50},
    #]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except(ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {
            "title": product.name + " - Online Store",
            "subtitle": product.name + " - Product information",
            "product": product
        }
        product = get_object_or_404(Product, pk=product_id) 
        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm):
    #name = forms.CharField(required=True, error_messages={"required": "Name is required."})
    #price = forms.FloatField(required=True, min_value=0.01, error_messages={"required": "Price is required.", "min_value": "Price must be greater than zero."})
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context