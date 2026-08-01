from django.urls import path
from payments import views

urlpatterns = [
    path('',                      views.checkout,     name='checkout'),
    path('callback/',             views.callback,     name='paytm_callback'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
]