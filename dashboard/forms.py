from django.contrib.auth.forms import UserCreationForm
from .models import User, GroupName, Category
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
