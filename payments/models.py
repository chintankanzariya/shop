import uuid
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]

    order_id            = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    product_name        = models.CharField(max_length=200)
    customer_name       = models.CharField(max_length=100)
    customer_email      = models.EmailField()
    customer_phone      = models.CharField(max_length=15)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    razorpay_order_id   = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} — ₹{self.amount} [{self.status}]"

    class Meta:
        ordering = ['-created_at']