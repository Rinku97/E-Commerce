from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Cutomer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  #one to one relationship is there which means tha a user can only have one cutomer and a cutomer can have only one user
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return  self.name    # this is the value that shows on our admin panel or when we create a model

#product order and order items
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)  # this digital is there because if there is a physical product then we will have to ship it other wise we will not.
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name   #returning the string value.

    @property         # this block of code is written because if delete an image of an item it will not produce an erro just give empty string instead of error
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


#Order Object:
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)  #Many to one relationship which means that customer cna have multiple orders
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=False)  #if complete is false that is an open cart we can add items into it, if its True This is the closed cart we needs to create items to differnet orders
    transaction_id = models.CharField(max_length=200, null=True)  #this is the extra informtion to our order

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            else:
                shipping == False
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#Order items
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)  #Many to one relationship
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)   # in order is our cart an order item is an item within our cart and the acrt cna have multiple order items that's why we need that many to one relationship
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name  #it will return the name value

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

#Shipping Address
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)   #if an order for some reason get deleted I would like to have a shipping address for a customer
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address  # returns th address