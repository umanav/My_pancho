from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        name = postData.get('name')
        username = postData.get('username')
        password = postData.get('password')
        confirm_password = postData.get('confirm_password')
        errors = []
        if len(name) < 1:
            errors.append("Name field can't be empty")
        elif len(name) < 3:
            errors.append("Name needs at least 3 characters")
        if len(username) < 1:
            errors.append("Username field can't be empty")
        elif len(username) < 3:
            errors.append("Username needs at least 3 characters")
        if len(password) < 1:
            errors.append("Password field can't be empty")
        elif len(password) < 9:
            errors.append("Password needs more than 8 characters")
        if password != confirm_password:
            errors.append("Passwords do not match")
        if errors == []:
            result = User.objects.filter(username=username)
            if len(result)>0:
                errors.append("Username already exists ")
                return errors
            else:
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                User.objects.create(name =name, username =username, password = password)
        return errors
    def login_validator(self, postData):
        username = postData.get('username')
        password = postData.get('password')
        errors = []
        if len(username) < 1:
            errors.append("Username field can't be empty")
        if len(password) < 1:
            errors.append("Password field can't be empty")
        if errors == []:
            try: 
                user = User.objects.get(username = username)
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    return errors
                errors.append("Invalid Username/Password")
            except User.DoesNotExist:
                errors.append("Invalid Username/Password")
        return errors
    def item_validator(self, postData):
        item = postData.get('item')
        errors = []
        if len(item) < 1:
            errors.append("Item field can't be empty")
        elif len(item) < 4:
            errors.append("Item field has to be more than 3 characters long")
        if errors == []:
            try: 
                whislist = Whishlist.objects.get(item = item)
                errors.append("WishList item is already stored")
                return errors
            except Whishlist.DoesNotExist:
                return errors
        return errors




class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<Blog object: {}>".format(self.name)

class Whishlist(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added_by = models.ForeignKey(User, related_name="Whishlist_item") 
    liked_by = models.ManyToManyField(User, related_name="whishlist_liked")
    objects = UserManager()
    def __repr__(self):
        return "<Blog object: {}>".format(self.item)