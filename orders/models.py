from django.db import models
from django.contrib.auth.models import User
from books.models import Books
from decimal import Decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Books, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def total_price(self):
        return Decimal(self.quantity * self.product.price if self.product else Decimal('0.00'))

