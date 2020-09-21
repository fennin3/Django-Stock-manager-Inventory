from django.db import models
from django.contrib.auth.models import User

CHOICES = (
    ('Available','Available'),
    ('Not Available','Not Available')
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    code = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    carton_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)
    unit_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)
    unit_quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=CHOICES, default="Available")
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def add_quantity(self, n): 
        return int(self.quantity) + int(n)
       

    def remove_quantity(self, n):
        if int(self.quantity) > 0 and int(self.quantity) >= int(n):
            return int(self.quantity) - int(n)
        else:
            return self.quantity

    def get_status(self):
        if self.quantity >0:
            
            return True
        else:
       
            return False

    def get_profit(self):
        profit = (self.unit_price * self.unit_quantity) - self.carton_price
        return profit
        

    


class Shop(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)
    

    def add_quantity(self, n):
        return int(self.quantity) + int(n)
    


    def __str__(self):
        return self.item.name


    def get_profit(self):
        profit = (self.quantity * self.item.unit_quantity * self.item.unit_price) - (self.item.carton_price * self.quantity)
        return profit
        

class ItemsIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} order "

    def order_profit(self):
        total = 0
        for item in self.items.all():
            total += item.get_profit()

        return total

    def total_products(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total


class ItemsOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Order)
    ordered_date = models.DateField(auto_now_add=True)

