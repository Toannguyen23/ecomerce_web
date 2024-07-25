
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)
admin.site.register(Category)