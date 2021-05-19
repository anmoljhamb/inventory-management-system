from django.contrib import admin
from .models import GroupName, Category, User, Product, OrderRequest, Order

# Register your models here.
admin.site.register(GroupName)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(OrderRequest)
admin.site.register(Order)