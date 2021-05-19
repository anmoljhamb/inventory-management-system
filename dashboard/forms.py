from django.contrib.auth.forms import UserCreationForm
from .models import User, GroupName, Category, Product, OrderRequest
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class GroupNameForm(forms.ModelForm):
    class Meta:
        model = GroupName
        fields = ['group_name']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone', 'password1', 'password2', 'image', 'user_type']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price_per_unit']

class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['product', 'staff', 'order_quantity', 'status']