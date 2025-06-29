from django.db import models
from django.contrib.auth.models import User
from app1.models import Product
from django.conf import settings
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', 
                               null=True, blank=True, 
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), 
                                               MaxValueValidator(100)])
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        if self.discount:
            return self.get_total_cost_before_discount() * self.discount/Decimal(100)
        return Decimal(0)
    class Meta:
        ordering = ['-created']

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    def get_total_price(self):
        return self.get_total_cost_before_discount() - self.get_discount()
    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name='items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity