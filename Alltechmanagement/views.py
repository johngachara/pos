from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from Alltechmanagement.forms import signin_form, products_form
from Alltechmanagement.models import Shop_stock


# Create your views here.
def signin(request):
    form = signin_form()
    if request.method== 'POST':
        form = signin_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return render(request,'home.html')
            else:
                messages.error(request,'Incorrect Username or Password')
                form = signin_form()
    return render(request,'signin.html',{"form":form})

@login_required
def homepage(request):
    products = Shop_stock.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{"page_obj":page_obj})

@login_required
def add_stock(request):
    form = products_form()
    if request.method == 'POST':
        form = products_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request,'Products cannot have the same name')
            form = products_form()
    return render(request,'addstock.html',{"Form":form})
