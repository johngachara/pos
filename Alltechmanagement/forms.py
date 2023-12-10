from django import forms

from Alltechmanagement.models import Shop_stock


class signin_form(forms.Form):
    username = forms.CharField(label='Username',max_length=30)
    password = forms.CharField(label='Password',max_length=30)

class products_form(forms.ModelForm):
    class Meta:
        model = Shop_stock
        fields = '__all__'
