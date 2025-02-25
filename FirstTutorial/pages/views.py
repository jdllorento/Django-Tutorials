from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ValidationError
# Create your views here.

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "Contact us - Online Store", 
            "subtitle": "Contact us", 
            "mail": "onlinestore@mail.com", 
            "address": "27th Street Park avn",
            "number": "+57 1234567890" 
        }) 
 
        return context

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
            "author": "Developed by: Your Name", 
        }) 
 
        return context

class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price":200}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":1000}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":100}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":50} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'products/show.html' 

    def get(self, request, id): 
        viewData = {} 
        
        # Verificar si el id es válido
        try:
            # Convertir el id a entero y restar 1 para obtener el índice
            product_index = int(id) - 1
            
            # Verificar si el índice está dentro del rango de la lista de productos
            if product_index < 0 or product_index >= len(Product.products):
                raise ValueError("Invalid product ID")
            
            # Obtener el producto
            product = Product.products[product_index]
            
        except (ValueError, IndexError):
            # Si el id no es válido, redirigir a la página de inicio
            return HttpResponseRedirect("/")
        
        # Si el id es válido, continuar con la lógica normal
        viewData["title"] = product["name"] + " - Online Store" 
        viewData["subtitle"] =  product["name"] + " - Product information" 
        viewData["product"] = product 

        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if (price <= 0):
            raise ValidationError("El precio debe ser mayor a 0")
        
        return price
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
             
            return HttpResponseRedirect(reverse('successfulcreation'))  
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)

class ProductCreated(TemplateView):
    template_name = "products/created.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "Success!!", 
            "subtitle": "Created item succesfully",
        }) 
 
        return context