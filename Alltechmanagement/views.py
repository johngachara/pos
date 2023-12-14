from base64 import b64encode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from Alltechmanagement.forms import signin_form, products_form, home_form, PaymentForm, CompleteForm
from Alltechmanagement.models import Shop_stock, Home_stock, Saved_transactions, Completed_transactions
import json
import logging

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Alltechmanagement import mpesa
from djangoProject15 import settings

logger = logging.getLogger(__name__)



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


@login_required
def initiate_payment(request):
    if request.method == "POST":
        till_number = request.POST['till']
        phone = request.POST["phone"]
        amount = request.POST["amount"]
        logger.info(f"{phone} {amount} {till_number}")
        timestamp = mpesa.get_current_timestamp()
        biz_short_code = till_number
        passkey = settings.MPESA_API["PASS_KEY"]
        password_string = biz_short_code + passkey + timestamp
        encoded_bytes = password_string.encode("ascii")
        password = b64encode(encoded_bytes).decode("utf-8")
        data = {
            "BusinessShortCode": till_number,
            "Password": password,
            "Timestamp": mpesa.get_current_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": till_number,
            "PhoneNumber": phone,
            "CallBackURL": mpesa.get_callback_url(),
            "AccountReference": "123456",
            "TransactionDesc": "Payment for merchandise"
        }
        headers = mpesa.generate_request_headers()

        resp = requests.post(mpesa.get_payment_url(), json=data, headers=headers)
        messages.success(request,'Prompt Sent Successfully')
        logger.debug(resp.json())
        json_resp = resp.json()
        if "ResponseCode" in json_resp:
            code = json_resp["ResponseCode"]
            if code == "0":
                mid = json_resp["MerchantRequestID"]
                cid = json_resp["CheckoutRequestID"]
                logger.info(f"{mid} {cid}")
            else:
                logger.error(f"Error while initiating stk push {code}")
        elif "errorCode" in json_resp:
            errorCode = json_resp["errorCode"]
            logger.error(f"Error with error code {errorCode}")
    return render(request, "payment.html")
@login_required
def callback(request):
    result = json.loads(request.body)
    logger.info(result)
    mid = result["Body"]["stkCallback"]["MerchantRequestID"]
    cid = result["Body"]["stkCallback"]["CheckoutRequestID"]
    code = result["Body"]["stkCallback"]["ResultCode"]
    logger.info(f"From Callback Result {mid} {cid} {code}")
    return HttpResponse({"message": "Successfully received"})
@login_required
def selling_page(request,product_id):
    product = Shop_stock.objects.get(pk=product_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            # Process the form data and save it to the database
            product_name = form.cleaned_data['product_name']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            Saved_transactions.objects.create(product_name=product_name, selling_price=price, quantity=quantity)
            product.quantity -= quantity
            product.save()


            # Here, you can save the data to your model or perform other actions
            # For example, assuming you have a Payment model:
            # Payment.objects.create(product_name=product_name, price=price, quantity=quantity)

            # Redirect to a success page or do anything else you need
            return redirect('home')
    return render(request,'sell.html',{"Product":product})
@login_required
def saved_transactions(request):
    transactions = Saved_transactions.objects.all()
    paginator = Paginator(transactions, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'transactions.html',{"page_obj":page_obj})
@login_required
def view_saved_transaction(request,transaction_id):
    transaction = Saved_transactions.objects.get(pk=transaction_id)
    return render(request,'viewtransactions.html',{"Product":transaction})
@login_required
def complete_transaction(request,transaction_id):
    transaction = Saved_transactions.objects.get(pk=transaction_id)
    transaction_name = transaction.product_name
    transaction_quantity = transaction.quantity
    transaction_price = transaction.selling_price
    Completed_transactions.objects.create(product_name=transaction_name, selling_price=transaction_price, quantity=transaction_quantity)
    transaction.delete()
    return redirect('home')
@login_required
def view_completed_transactions(request):
    transactions = Completed_transactions.objects.all()
    paginator = Paginator(transactions, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'completed.html', {"page_obj": page_obj})
@login_required
def delete_saved_transactions(request,transaction_id):
    transaction = Saved_transactions.objects.get(pk=transaction_id)
    transaction.delete()
    messages.error(request,f"{transaction} deleted Successfully")
    return redirect('transactions')

