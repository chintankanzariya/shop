from django.contrib import admin
from .models import Product, Orders, OrderUpdate, Contact


# admin.site.register(Product)
# admin.site.register(Contact)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "product_name", "dec","pu_date", "category", "subcategory", "image","price",]
    search_fields = ('product_name', 'category')





@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["order_id","items_json","name","email","address","city","state","zip_code","amount"]
    search_fields = ('order_id', 'email', 'name', 'phone')

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ["update_id","update_desc","timestamp"]
    search_fields = ('order_id',)







@admin.register(Contact)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ["msg_id","name","email","phone","desc"]
    search_fields = ('msg+id',)