from django import forms

from Alltechmanagement.models import Shop_stock, Home_stock


class signin_form(forms.Form):
    username = forms.CharField(label='Username',max_length=30)
    password = forms.CharField(label='Password',max_length=30,widget=forms.PasswordInput(attrs={"type":"password"}))

class products_form(forms.ModelForm):
    class Meta:
        model = Shop_stock
        fields = '__all__'



class home_form(forms.ModelForm):
    class Meta:
        model = Home_stock
        fields = '__all__'

class PaymentForm(forms.Form):
    product_name = forms.CharField(max_length=255)
    price = forms.DecimalField()
    quantity = forms.IntegerField()


class CompleteForm(PaymentForm):
    pass
