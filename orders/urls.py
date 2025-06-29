from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order', views.order_create, name='create_order'),
    path('admin/order/<int:order_id>', views.admin_order_detail, name='admin_order_detail'),
]