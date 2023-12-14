from django.urls import path
from . import views
urlpatterns = [
    path('signin',views.signin,name='signin'),
    path('',views.homepage,name='home'),
    path('addstock',views.add_stock,name='add_stock'),
    path('signout',views.signout,name='signout'),
    path('homestock',views.home_stock,name='home_stock'),
    path('addhomestock',views.add_home_stock,name='add_home'),
    path('product/<int:product_id>',views.view_product,name='product'),
    path('update/<int:product_id>',views.update_product,name='update'),
    path('delete/<int:product_id>',views.delete_product,name='delete'),
    path('search',views.search_product,name='search'),
    path('homesearch',views.search_home_stock,name='search_home'),
    path('homeproductview/<int:product_id>',views.view_home_stock,name='view_home_stock'),
    path('updatehome/<int:product_id>',views.update_home_stock,name='update_home'),
    path('deletehome/<int:product_id>',views.delete_home_stock,name='delete_home'),
    path('dispatchpage/<int:product_id>',views.dispatch_page,name='dispatch_page'),
    path('dispatch/<int:product_id>',views.dispatch,name='dispatch'),
    path('mpesa', views.initiate_payment, name="initiate"),
    path('callback', views.callback, name="callback"),
    path('sell/<int:product_id>',views.selling_page,name='sell'),
    path('transactions',views.saved_transactions,name='transactions'),
    path('view_transactions/<int:transaction_id>',views.view_saved_transaction,name='view_transaction'),
    path('complete/<int:transaction_id>',views.complete_transaction,name='complete'),
    path('view_complete',views.view_completed_transactions,name='view_complete'),
    path('delete_saved/<int:transaction_id>',views.delete_saved_transactions,name='delete_saved')
]