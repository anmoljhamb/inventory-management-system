from django.db import models
from django.contrib.auth.models import User as AbstractUser
from django.contrib.auth.models import Group


ORDER_CHOCIES = (
    ('APPROVED', 'APPROVED'),
    ('DENIED', 'DENIED'),
    ('PENDING', 'PENDING'),
)


class GroupName(models.Model):
    group_name = models.CharField(max_length=100, unique=True, error_messages={'unique': "Error while creating the account. A shop with that name already exists."})
    class Meta:
        verbose_name_plural = "GroupNames"
    def __str__(self):
        return self.group_name

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True, error_messages={'unique': "Category with duplicate name cannot exist."})
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    price_per_unit = models.PositiveIntegerField(null=True)
    total_sale = models.PositiveIntegerField(default=0)


    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)


    def __str__(self):
        return f'{self.name}({self.quantity}) Rs {self.price_per_unit}/unit'



'''
User Models
'''
class User(AbstractUser):
    image = models.ImageField(default='avatar.png', upload_to='profile_images')
    name = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=20, null=True)
    
    user_type = models.CharField(max_length=100, null=True, choices=[("User", "User"), ("Group Admin", "Group Admin")], default="User")
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user_type}: {self.username}'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._meta.get_field('user_type').choices = [(x.name, x.name) for x in Group.objects.all()]
'''
End User Models
'''
class OrderRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=ORDER_CHOCIES, default="Pending")
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE, null=True)
    total_amount = models.PositiveIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(OrderRequest, self).__init__(*args, **kwargs)

    def __str__(self):
        return f'{self.order_quantity} {self.product} ordered by {self.staff}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE, null=True)
    total_amount = models.PositiveIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)

    def __str__(self):
        return f'{self.order_quantity} {self.product} ordered by {self.staff}'