from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import AddToCartForm

def product_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category, available=True)
    
    
    context = {'products': products, 'category': category, 'categories': categories}
    return render(request, 'app1/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_form = AddToCartForm()
    context = {'product': product, 'cart_form': cart_form}
    return render(request, 'app1/product/detail.html', context)