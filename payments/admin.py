from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ['order_id', 'customer_name', 'amount', 'status', 'razorpay_payment_id', 'created_at']
    list_filter     = ['status']
    search_fields   = ['order_id', 'customer_name', 'customer_email']
    readonly_fields = ['order_id', 'razorpay_order_id', 'razorpay_payment_id']