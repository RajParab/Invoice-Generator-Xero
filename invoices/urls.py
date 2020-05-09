#from django.contrib import admin
from django.urls import path
from . import views
app_name='invoices'


urlpatterns = [
    path('', views.invoiceView, name='invoiceView'),
    path('success',views.success,name='success'),
]
