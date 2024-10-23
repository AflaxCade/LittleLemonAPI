from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(default="", null=False)
    title = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitems = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuitems')
    
    def __str__(self):
        return f"Cart: {self.user.username} - {self.menuitems.title} (x{self.quantity})"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        delivery_status = 'Assigned' if self.delivery_crew else 'Not Assigned'
        order_status = 'Completed' if self.status else 'Pending'
        return f"Order #{self.id} by {self.user.username} - {order_status}, Delivery: {delivery_status}, Total: ${self.total}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
         return f"{self.quantity} x {self.menuitem.title} for Order #{self.order.id} - Unit Price: ${self.unit_price}, Total: ${self.price}"