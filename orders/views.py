from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                order_item = OrderItem.objects.create(order=order, product=item['product'], 
                                                      quantity=item['quantity'], price = item['price'])
                order_item.save()

            cart.clear()
            # Execute tasks asynchroniously
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    context = {'form': form, 'cart': cart}
    return render(request, 'orders/create.html', context)
