from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from math import ceil
from django.urls import path
from .models import Product,  Orders, OrderUpdate,Contact
import json
from urllib.parse import urlencode
from django.urls import reverse
def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'product_id')
    categories = {item['category'] for item in catprods}

    for cat in categories:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = ceil(n / 4)
        allprods.append([prod, range(1, nslides), nslides])

    return render(request, "shop/index.html", {'allprods': allprods})


def searchMatch(query,item):
    if query in item.dec.lower() or query in item.product_name.lower() or query in item.category.lower():
          return True
    else:
          return False
def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, "shop/about.html")




def product(request, my_product_id):
    products = Product.objects.get(product_id=my_product_id)
    return render(request, "shop/product.html", {"products": products})



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')






def checkout(request):
    if request.method == "POST":
        name       = request.POST.get("name", "")
        amount     = request.POST.get("amount", "")
        email      = request.POST.get("email", "")
        phone      = request.POST.get("phone", "")
        address    = request.POST.get("address", "")
        city       = request.POST.get("city", "")
        state      = request.POST.get("state", "")
        zip_code   = request.POST.get("zip_code", "")
        items_json = request.POST.get('items_json', '')

        if not name or not email:
            return render(request, 'shop/checkout.html', {'error': 'Name and Email are required'})

        order = Orders(
            items_json = items_json,
            name       = name,
            email      = email,
            address    = address,
            city       = city,
            state      = state,
            zip_code   = zip_code,
            phone      = phone,
            amount     = amount,
        )
        order.save()

        update = OrderUpdate(
            order_id    = order.order_id,
            update_desc = "The Order has been placed"
        )
        update.save()

        params = urlencode({
            'name'   : name,
            'email'  : email,
            'phone'  : phone,
            'amount' : amount,
            'product': f'Order #{order.order_id}',
        })
        return redirect(f"/payments/?{params}")  # ✅

    return render(request, 'shop/checkout.html')






def product_json(request, product_id):
    try:
        p = Product.objects.get(product_id=product_id)
        return JsonResponse({
            'name': p.product_name,
            'price': float(p.price),
            'image': str(p.image),
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('home')

def contact(request):
    if request.method == "POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        print(name,email,phone, desc )
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html")







def compare_product(request, my_product_id):
    try:
        product1 = Product.objects.get(product_id=my_product_id)

        # get all other products in the same category (for dropdown options)
        same_category_products = Product.objects.filter(
            category=product1.category
        ).exclude(product_id=my_product_id)

        # check if user picked a specific product2 via dropdown (GET param)
        compare_id = request.GET.get('compare_id')

        if compare_id:
            product2 = Product.objects.filter(product_id=compare_id).first()
        else:
            product2 = same_category_products.first()

        return render(request, 'shop/compare_product.html', {
            'product1': product1,
            'product2': product2,
            'same_category_products': same_category_products,
        })

    except Product.DoesNotExist:
        return render(request, 'shop/compare_product.html', {
            'error': 'Product not found'
        })