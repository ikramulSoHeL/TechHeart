from math import ceil
from msilib.schema import ListView

from django.db.models import Q
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
import json

import datetime


def home(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:

        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }


    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'products': products,
        'items': items,
        'order':order,
        'categories':categories,

    }

    return render(request, 'store/home-page.html', context)


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        # else:
        # return render(request, 'user/login.html', {'form': form})
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'store/account/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            Customer.objects.create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
        else:
            context = {
                "form": form,
            }

            return render(request, 'store/account/register.html', context)

    form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, 'store/account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def checkout_view(request):

    if request.user.is_authenticated:
        products = Product.objects.all()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }

    products = Product.objects.all()
    context = {
                  'products': products,
                  'items': items,
                  'order': order,
    }

    return render(request, 'store/checkout-page.html', context)



def payment_view(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }

    products = Product.objects.all()
    context = {
                  'products': products,
                  'items': items,
                  'order': order,
    }

    return render(request, 'store/payment.html', context)


def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
        }


    context = {'items': items, 'order': order}
    return render(request, 'store/shopping-bag.html', context)


def updateItem_view(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = -1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)


def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }


    context = {
        'product': product,
        'items': items,
        'order': order,
    }
    return render(request, 'store/product-page.html', context)


def category_product_view(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }
    products = Product.objects.filter(category=pk)
    products2 = Product.objects.all()
    context = {
        'products': products,
        'items': items,
        'order': order,
        'products2': products2
    }
    return render(request, 'store/category_product-page.html', context)

def all_product_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }


    products= Product.objects.all()
    context = {
        'products': products,
        'items': items,
        'order': order,

    }
    return render(request, 'store/category_product-page.html', context)

def search_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,

        }

    k = request.GET.get('k')
    p = request.GET.get('p')
    if not p:
        p = 999999999999999

    sorting = request.GET.get('sorting', '-price')

    products = Product.objects.filter(Q(name__icontains=k) | Q(category__category_name__icontains=k)).filter(price__lte=p)

    context = {
        'products':  products.order_by(sorting),
        'items': items,
        'order': order,

    }
    return render(request, 'store/category_product-page.html', context)


def blog_view(request):

    all = Blog.objects.all().order_by('publish_date')

    return render(request, 'store/blog.html', {'all':all})

def blog_detail_view( request, pk):
    blog = Blog.objects.get(id=pk)

    return render(request, 'store/blog-detail.html', {'blog': blog})

def contact_us_view(request):
    if request.method == "POST":
        name = request.POST.get('txtName')
        email = request.POST.get('txtEmail')
        phone = request.POST.get('txtPhone')
        msg = request.POST.get('txtMsg')
        #send email
        send_mail(
            'Message From' + ' ' + name + ' ' + phone, # subject
            msg, # message
            email, # from_email
            ['techhearthelp@gmail.com'], # to_email
        )
        return render(request, 'store/contact_us.html', {'name':name})
    return render(request, 'store/contact_us.html')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        Delivery.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            phone=data['shipping']['phone'],
            trxId=data['shipping']['trxId'],
        )

    else:
        print('User is not logged in....')

    return JsonResponse('Payment submitted..', safe=False)
