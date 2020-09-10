from django.contrib import admin
from .models import Product, Category, Shop, Item, ItemsIn

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(ItemsIn)
