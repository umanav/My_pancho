from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
def index(request):
    if 'id' in request.session == None:
        return redirect('/home')
    if 'id' in request.session:
        return redirect('/home')
    return render(request,'My_app/main.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = User.objects.last().id
        return redirect('/home')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        user = User.objects.get(username = request.POST['username'])
        request.session['id'] = user.id
        return redirect('/home')

def logout(request):
    del request.session['id']
    return redirect('/')

def home(request):
    id=request.session['id']
    user = User.objects.get(id=id)
    My_wishlist = []
    for user_likes in  user.whishlist_liked.all() :
        My_wishlist.append(user_likes)
    Other_wishlist = []
    for users in User.objects.all() :
        likes = users.whishlist_liked.exclude(liked_by=id)
        for like in likes:
            if like not in My_wishlist:
                if like not in Other_wishlist:
                    Other_wishlist.append(like)
    return render(request,'My_app/home.html', {'user' : user , 'My_wishlist': My_wishlist, 'Other_wishlist' : Other_wishlist})

def add(request):
    return render(request,'My_app/add_wishlist.html')

def create(request):
    errors = User.objects.item_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/add')
    else:
        id = request.session['id']
        user = User.objects.get(id = id)
        wish_item = Whishlist.objects.create(item=request.POST['item'], added_by=user)
        wish_item.liked_by.add(user)
        return redirect('/home')

def add_item(request,id):
    userid = request.session['id']
    user = User.objects.get(id = userid)
    user.whishlist_liked.add(id)
    return redirect('/home')

def remove_item(request,id):
    userid = request.session['id']
    user = User.objects.get(id = userid)
    user.whishlist_liked.remove(id)
    return redirect('/home')

def delete_item(request,id):
    item = Whishlist.objects.get(id=id)
    item.delete()
    return redirect('/home')

def display_product(request,id):
    item = Whishlist.objects.get(id=id)
    product_likes = []
    for users in User.objects.all() :
        if not users.whishlist_liked.filter(id=id):
            pass
        else:
            product_likes.append(users.name)
    return render(request,'My_app/product.html', {"product_likes" : product_likes, 'item' : item})
