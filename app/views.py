from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime


def home(request):
     if request.user.is_authenticated:
        customer = request.user 
        order, created = Orders.objects.get_or_create(customer = customer, complete = False)
        items = OrderItems.objects.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
     else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_cart_items':0, 'get_total': 0, "shipping" : False}
        cartItems = order['get_cart_items']
     products = Products.objects.all()
     categories = Category.objects.filter(is_sub = False)
     active_category = request.GET.get('category', '')
     context ={"products": products,
               "cartItems": cartItems,
               "user_login": user_login, 
               "user_not_login": user_not_login,
               "categories": categories,
               "active_category": active_category,
               
               
               }
     
     return render(request, 'app/home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user 
        order, created = Orders.objects.get_or_create(customer = customer, complete = False)
        items = OrderItems.objects.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        
    else:
        items = []
        order = {'get_cart_items':0, 'get_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
            
            
            
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    context ={'items': items,
              'order': order,
              'cartItems': cartItems,
              'user_login': user_login,
              'user_not_login': user_not_login,
              'categories': categories,
              'active_category': active_category
              }
    
    return render(request, 'app/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user 
        order, created = Orders.objects.get_or_create(customer = customer, complete = False)
        items = OrderItems.objects.all()
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_cart_items':0, 'get_total': 0, "shipping" : False}
    context ={'items': items,
              'order': order,
              'user_not_login': user_not_login,
              'user_login': user_login
              }
    return render(request, 'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Products.objects.get(id=productId)
    order, created = Orders.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItems.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
       orderItem.quantity += 1
    elif action == 'remove':
       orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    if processOrder:
        if order.complete == True:
            orderItem.delete()
        
    return JsonResponse('added',safe=False)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context )


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username hoặc mật khẩu đăng nhập không chính xác")
    context = {}
    return render(request, 'app/login.html', context )

def logoutPage(request):
    logout(request)
    return redirect("login")

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Products.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user 
        order, created = Orders.objects.get_or_create(customer = customer, complete = False)
        items = OrderItems.objects.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_cart_items':0, 'get_total': 0}
        cartItems = order['get_cart_items']
    products = Products.objects.all()
    
    context ={"products": products, "cartItems": cartItems, "user_login": user_login, "user_not_login": user_not_login}
    return render(request, 'app/search.html', {'searched': searched, 'keys': keys,"products": products, "cartItems": cartItems})


def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    
    if active_category:
        products = Products.objects.filter(category__slug = active_category)
    context = {'categories': categories, 'products': products, 'active_category': active_category}
    
    return render(request, 'app/category.html', context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp() 
    data = json.loads(request.body)   
    if request.user.is_authenticated:
        customer = request.user
        order, created = Orders.objects.get_or_create(customer = customer, complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
            
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                mobile = data['shipping']['phone'],
            )
            
        
    else:
        print("Người dùng chưa đăng nhập")
            
    return JsonResponse("Payment complete..", safe=False)