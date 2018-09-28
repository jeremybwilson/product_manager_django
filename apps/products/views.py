# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Product
import re, bcrypt

# Create your views here.
def index(request):


    product_list = Product.objects.all()
    context = {
        'products': product_list
    }
    return render(request, 'products/index.html', context)

def new(request):
    
    return render(request, 'products/new.html')

def create(request):
    
    return redirect('products:index')

def show(request, user_id):
    pass

def edit(request, user_id):
    pass

def update(request, user_id):
    pass

def delete(request, user_id):
    pass

def login(request):
    if request.method == "POST":
        pass
    else:
        return redirect('products:new')

def logout(request):
  request.session.clear()
  return redirect('products:index')