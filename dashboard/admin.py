from django.contrib import admin
from .models import GroupName, Category, User, Product, OrderRequest, Order


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group_name")
    list_filter = ["group_name"]


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "user_type", "group_name", "image")
    list_filter = ["user_type", "group_name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group_name",
        "category",
        "quantity",
        "price_per_unit",
        "total_sale",
    )
    list_filter = ("group_name",)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "staff",
        "order_quantity",
        "date",
        "group_name",
        "total_amount",
    )
    list_filter = ["group_name"]


class OrderReqAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "staff",
        "order_quantity",
        "date",
        "group_name",
        "total_amount",
        "status",
    )
    list_filter = ["group_name", "status"]


class GroupNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)

admin.site.register(GroupName)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderRequest, OrderReqAdmin)
admin.site.register(Order, OrderAdmin)
