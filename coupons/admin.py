from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount']
    list_filter = ['active', 'valid_from', 'valid_to']
    serach_fields = ['code']
