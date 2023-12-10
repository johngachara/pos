from django.urls import path
from . import views
urlpatterns = [
    path('signin',views.signin,name='signin'),
    path('',views.homepage,name='home'),
    path('addstock',views.add_stock,name='add_stock')
]