from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from Alltechmanagement.forms import signin_form, products_form, home_form
from Alltechmanagement.models import Shop_stock, Home_stock


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
                return redirect('home')
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
@login_required
def signout(request):
    logout(request)
    return redirect('signin')
@login_required
def home_stock(request):
    products = Home_stock.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'homestock.html',{"page_obj":page_obj})
@login_required
def add_home_stock(request):
    form = home_form()
    if request.method == 'POST':
        form = home_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_stock')
        else:
            messages.error(request, 'Products cannot have the same name')
            form = home_form()
    return render(request, 'addhomestock.html', {"Form": form})
@login_required
def view_product(request,product_id):
    product = Shop_stock.objects.get(pk=product_id)
    return render(request,'product.html',{"Product":product})

@login_required
def update_product(request,product_id):
    to_update = Shop_stock.objects.get(pk=product_id)
    form = products_form(instance=to_update)
    if request.method == 'POST':
        form = products_form(request.POST,instance=to_update)
        if form.is_valid():
            form.save()
            return redirect('product',product_id)
        else:
            form = products_form(instance=to_update)
    return render(request,'update.html',{"Form":form})
@login_required
def delete_product(request,product_id):
    to_delete = Shop_stock.objects.get(pk=product_id)
    to_delete.delete()
    messages.error(request,f"{to_delete} Deleted Succesfully")
    return redirect('home')

@login_required
def search_product(request):
    search_parameter = request.GET.get('Searching')
    data = Shop_stock.objects.filter(Q(product_name__icontains=search_parameter))
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{"page_obj":page_obj})
@login_required
def search_home_stock(request):
    search_parameter = request.GET.get('Home_stock_searching')
    data = Home_stock.objects.filter(Q(product_name__icontains=search_parameter))
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'homestock.html', {"page_obj": page_obj})
@login_required
def view_home_stock(request,product_id):
    product = Home_stock.objects.get(pk=product_id)
    return render(request,'homeproduct.html',{"Product":product})
@login_required
def update_home_stock(request,product_id):
    toupdate = Home_stock.objects.get(pk=product_id)
    form = home_form(instance=toupdate)
    if request.method == 'POST':
        form = home_form(request.POST,instance=toupdate)
        if form.is_valid():
            form.save()
            messages.success(request,f"{toupdate} updated Successfully")
            return redirect('view_home_stock',product_id)
        else:
            form = home_form(instance=toupdate)
    return render(request,'updatehome.html',{"Form":form})
@login_required
def delete_home_stock(request,product_id):
    to_delete = Home_stock.objects.get(pk=product_id)
    to_delete.delete()
    messages.error(request, f"{to_delete} Deleted Successfully")
    return redirect('home_stock')

@login_required
def dispatch_page(request, product_id):
    try:
        product = Home_stock.objects.get(pk=product_id)
        return render(request, 'dispatch.html', {"Product": product})
    except Home_stock.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('homeproduct')

@login_required
def dispatch(request,product_id):
    product = Home_stock.objects.get(pk=product_id)
    quantity = request.GET.get('dispatch_quantity')
    if product.quantity > 0 :
        product.quantity -= int(quantity)
        product.save()
        return redirect('home_stock')
    else:
        messages.error(request,'No stock left in database')
        return redirect('home_stock')