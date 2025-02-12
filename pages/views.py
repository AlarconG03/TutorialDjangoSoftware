from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django import forms

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

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 500},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 300},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 99},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 50},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        if not id.isdigit() or int(id) not in range(1, len(Product.products) + 1):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        viewData["price"] = product["price"]

        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True, error_messages={"required": "Name is required."})
    price = forms.FloatField(required=True, min_value=0.01, error_messages={"required": "Price is required.", "min_value": "Price must be greater than zero."})

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"title": "Create product", "form": form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return render(request, "products/created.html", {"title": "Product Created"})
        return render(request, self.template_name, {"title": "Create product", "form": form})