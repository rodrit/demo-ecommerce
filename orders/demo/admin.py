from django.contrib import admin
from .models import Product, Order, OrderDetail

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Product)
