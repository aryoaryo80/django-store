from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def final_price(self):
        if self.discount:
            return int(self.discount / 100 * self.get_total_price())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id} {self.get_cost()}'

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=100)
    discount = models.PositiveIntegerField(
        validators=(MaxValueValidator(100),))
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f'{self.code}'
