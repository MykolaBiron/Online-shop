from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from app1.models import Product
from .forms import AddToCartForm
from coupons.forms import CouponApplyForm

@require_POST
def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    form = AddToCartForm(request.POST)
    cart = Cart(request)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], 
                 override_quantity=cd['override'])
    return redirect("cart:cart_detail")

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    coupon_form = CouponApplyForm()
    for item in cart:
        item['update_quantity_form'] = AddToCartForm(initial={'quantity': item['quantity'], 
                                                              'override': True})
    context = {'cart': cart, 'coupon_form': coupon_form}
    return render(request, 'cart/detail.html', context)


