from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.views import get_user_model
from django.core.validators import MinValueValidator

from .tasks import sent_email

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Fix the field name


class Files(models.Model):
    file = models.FileField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField()
    website = models.URLField()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
