# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
# from ..products.models import Product
import re, bcrypt

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('users:new')

    if 'logged_id' not in request.session:
        return redirect('users:new')
    
    # find the user id of the logged in user
    user_id = int(request.session['user_id'])
    # print "*" * 80
    # print "Here is the USER ID from session:", user_id
    user_list = User.objects.all()
    specific_user = User.objects.get(id=user_id)
    # print "*" * 80
    # print "Here is the specific user from db:", specific_user

    context = {
        'users': user_list,
        'specific_user_id': specific_user.id,
        'name': specific_user.name
    }

    print "*" * 80
    print context
    # print "Session User ID for this route is: ", user_id
    print "Session Logged ID for this route is: ", request.session['logged_id']

    return render(request, 'users/index.html', context)

def new(request):
    return render(request, 'users/new.html')

def create(request):
    if request.method == 'POST':

        valid, result = User.objects.validate_and_create_user(request.POST)
        print "*" * 80
        print "Successfully entered the create route."
        print valid
        print result
        
        if valid:
            request.session['user_id'] = result
            return redirect('users:index')
        else:
            for error in result:
                messages.error(request, error)
            return redirect('users:new')
    else:
        return redirect('users:new')


def show(request, user_id):

    if 'user_id' not in request.session:
        return redirect('users:new')
    else:
        # print the user_id, "THIS IS THE USER_ID"
        print "THIS IS THE USER_ID", request.session['user_id']

        user_id = int(user_id)
        try:
            user = User.objects.get(id=user_id)
            # print "Try statement block => user info: ", user
        except:
            return redirect('users:index')

        if 'logged_id' not in request.session:
            logged_id = request.session['logged_id']
        else:
            logged_id = request.session['user_id']

        context = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            'permission_level': user.permission_level,
            'specific_user_id': user.id,
            'created_products': user.created_products.all(),
            'products': user.products.all()
        }

        # redirect_url = str('users/') + str(user_id) + str('/show.html')
        # return render(request, redirect_url, context)
        return render(request, 'users/show.html', context)

def edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect('users:new')

    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect('users:index')

    # name = form_data['name']
    context = {
        'user': user,
        'name': user.name,
        # "permission_level": user.permission_level
    }
    return render(request, 'users/edit.html', context)

def update(request, user_id):
    if request.method == 'POST':
        valid, result = User.objects.validate_and_update_user(user_id, request.POST)
        if not valid:
            for error in result:
                messages.error(request, error)
            return redirect('users:edit', user_id=user_id)

    return redirect('users:index')

def delete(request, user_id):
    if request.method == 'POST':
        User.objects.delete_user_by_id(user_id)
    return redirect('users:index')

def login(request):
    if request.method == "POST":

        valid, result = User.objects.login_user(request.POST)
        if not valid:
            for error in result:
                messages.error(request, error)
            return redirect('users:new')
        else:
            request.session['user_id'] = result
            request.session['logged_id'] = result
            # print "=" * 80
            # print "login route user_id is: ", result
            return redirect('users:index')
    else:
        return redirect('users:new')

def logout(request):
  request.session.clear()
  return redirect('users:index')