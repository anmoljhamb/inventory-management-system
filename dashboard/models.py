from django.db import models
from django.contrib.auth.models import User as AbstractUser
from django.contrib.auth.models import Group


class GroupName(models.Model):
    group_name = models.CharField(max_length=100, unique=True, error_messages={'unique': "Error while creating the account. A shop with that name already exists."})
    class Meta:
        verbose_name_plural = "GroupNames"
    def __str__(self):
        return self.group_name

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return f'{self.name} by group {self.group_name}'

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