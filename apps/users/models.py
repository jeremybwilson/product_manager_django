# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from ..products.models import Product
import re, bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_and_create_user(self, form_data):
        errors = []

        name = form_data['name']
        username = form_data['username']
        email = form_data['email']
        password = form_data['password']
        confirm_password = form_data['confirm_password']

        if len(name) < 1:
            errors.append('Name cannot be blank.')
        if len(name) < 2:
            errors.append('Name must be longer than 2 characters.')        
        if len(username) < 1:
            errors.append('Username cannot be blank.')
        if len(username) < 2:
            errors.append('Username must be longer than 2 characters.')
        if len(email) < 1:
            errors.append('Email cannot be blank.')
        elif not EMAIL_REGEX.match(email):
            errors.append('You must enter a valid email address!')
        if len(password) < 1:
            errors.append('Password cannot be blank.')
        if len(password) < 3:
            errors.append('Password must be at least 3 characters long.')
        if len(confirm_password) < 1:
            errors.append('Confirm password cannot be blank.')
        if password != confirm_password:
            errors.append('Passwords do not match!')

        username_list = User.objects.filter(username=username)

        if len(username_list) > 0:
            errors.append('Username already in use.  Please choose another.')

        try:
            user = User.objects.get(email=email)
            errors.append('Email already in use.  Please choose another')
            return (False, errors)
        except:
            if len(errors) > 0:
                return (False, errors)
            else:
                # REMEMBER TO HASH THE PASSWORD
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User.objects.create(name=name, username=username, email=email, pw_hash=pw_hash, permission_level="STUDENT")
                return (True, user.id)

        return (True, user.id)

        # REMEMBER TO HASH THE PASSWORD
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_and_update_user(self, user_id, form_data):
        errors = []

        name = form_data['name']
        email = form_data['email']

        if len(name) < 2:
            errors.append('Name must be at least 2 characters')
        if not EMAIL_REGEX.match(email):
            errors.append('Must use a valid email address')

        if errors:
            return (False, errors)

        try:
            user = self.get(id=user_id)
            user.name = form_data['name']
            user.email = form_data['email']
            user.save()
            return (True, user)
        except:
            errors.append("User doesn't exist")
            return (False, errors)

    def login_user(self, form_data):
        errors = []

        # username = form_data['username']
        email = form_data['email']
        password = form_data['password']

        try:
            user = User.objects.get(email=email)
            # user = User.objects.get(email=email)
            # check to see if passwords match
            if not bcrypt.checkpw(password.encode(), user.pw_hash.encode()):
                errors.append('Username or password is invalid')
                return (False, errors)
                print "Errors occurred during password validation"

            # username_list = User.objects.filter(username=username)

            return (True, user.id)
        except:
            errors.append('Username or password is invalid')
            return (False, errors)

    def delete_user_by_id(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except:
            return False

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    permission_level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def __str__(self):
    output = "<User object: {}>".format(self.email)
    # output = "<User object: {}>".format(self.username)
    return self.output
