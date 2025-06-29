from celery import shared_task
from .models import Order
from django.core.mail import send_mail

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    mail = send_mail(f"You order", 
                     "You order number {order_id} was successfully placed. Thank you!", 
                     "mykolabiron@gmail.com",
                     [order.email])
    return mail