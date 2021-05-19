from django.contrib import admin
from .models import GroupName, Category, User

# Register your models here.
admin.site.register(GroupName)
admin.site.register(Category)
admin.site.register(User)