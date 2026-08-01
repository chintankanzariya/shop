import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def checkout(request):
    print("REQUEST METHOD:", request.method)
    print("GET DATA:", request.GET)
    print("POST DATA:", request.POST)

    name    = ''
    email   = ''
    phone   = ''
    amount  = ''
    product = ''

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        amount  = request.POST.get('amount', '').strip()
        product = request.POST.get('product', 'Order').strip()

    elif request.method == 'GET':
        name    = request.GET.get('name', '').strip()
        email   = request.GET.get('email', '').strip()
        phone   = request.GET.get('phone', '').strip()
        amount  = request.GET.get('amount', '').strip()
        product = request.GET.get('product', 'Order').strip()
        print("GET params:", name, email, phone, amount, product)

    if not all([name, email, phone, amount]):
        print("MISSING FIELDS - showing form")
        return render(request, 'payments/razorpay_checkout.html')

    # Amount in paise
    amount_paise = int(float(amount) * 100)
    print("Amount paise:", amount_paise)

    # Razorpay max limit check
    if amount_paise > 50000000:
        messages.error(request, f'Amount ₹{amount} exceeds maximum ₹5,00,000.')
        return render(request, 'payments/razorpay_checkout.html')

    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount'         : amount_paise,
        'currency'       : 'INR',
        'payment_capture': 1
    })
    print("Razorpay order created:", razorpay_order['id'])

    # Save in DB
    order = Order.objects.create(
        customer_name     = name,
        customer_email    = email,
        customer_phone    = phone,
        amount            = amount,
        product_name      = product,
        razorpay_order_id = razorpay_order['id'],
    )
    print("Order saved:", order.order_id)

    context = {
        'order'        : order,
        'razorpay_key' : settings.RAZORPAY_KEY_ID,
        'amount_paise' : amount_paise,
        'name'         : name,
        'email'        : email,
        'phone'        : phone,
        'product'      : product,
        'amount'       : amount,
    }
    return render(request, 'payments/razorpay_checkout.html', context)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id   = request.POST.get('razorpay_order_id', '')
        razorpay_signature  = request.POST.get('razorpay_signature', '')

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return render(request, 'payments/payment_status.html', {
                'status' : 'ERROR',
                'message': 'Order not found.',
            })

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id'  : razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature' : razorpay_signature,
            })
            order.status              = 'SUCCESS'
            order.razorpay_payment_id = razorpay_payment_id
            order.save()
        except Exception:
            order.status = 'FAILURE'
            order.save()

        return render(request, 'payments/payment_status.html', {
            'order'  : order,
            'status' : order.status,
            'txn_id' : order.razorpay_payment_id,
            'amount' : str(order.amount),
            'message': 'Payment Successful!' if order.status == 'SUCCESS' else 'Payment Failed.',
        })

    return redirect('checkout')


def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'payments/payment_status.html', {
        'order' : order,
        'status': order.status,
    })