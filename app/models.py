from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Category(models.Model):
        
    sub_category = models.ForeignKey('self', on_delete= models.CASCADE, related_name='sub_categories', null = True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=150, null=True)
    slug = models.SlugField(max_length=150, unique=True)
        
    def __str__(self):
    
        return self.name
class Products(models.Model):
    
    category = models.ManyToManyField(Category, related_name="product_category")
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        
        return self.name
    
    
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
class Orders(models.Model):
    
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null = True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=150, null=True)
    
    
    def __str__(self) -> str:
        
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        
        return total
    
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        
        return total
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitems_set.all()
        for i in orderitems:
            if i.product.digital == False:
               shipping = True
                
        return shipping
class OrderItems(models.Model):
    
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, blank=True, null = True)
    quantity = models.IntegerField(default=0, null= True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        
        return total
    
class ShippingAddress(models.Model):
    
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, blank=True, null = True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.address
    
    
