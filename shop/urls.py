from django.urls import path, include
from shop import views


urlpatterns=[
    path("index",views.index,name="index"),
    path("about",views.about,name="about"),
    path("contact/",views.contact,name='contact'),
    path("tracker/",views.tracker,name="tracker"),
    path("search/",views.search,name="search"),
    path("products/<int:my_product_id>",views.product,name="product"),
    path('checkout/', views.checkout, name='checkout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
path('compare/<int:my_product_id>/', views.compare_product, name='compare_products'),
]







