from django.contrib import admin
from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail')
]