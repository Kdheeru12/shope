# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False,unique=True,max_length=254,verbose_name='email')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD='email'

WEBURLS  = (
    ('electronic','electronic'),
    ('beauty','beauty'),
    ('food','food'),
    ('fashion','fashion'),
    ('sports','sports'),
)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=300,blank=True,null=True)
    email = models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return self.user.username
class Product(models.Model):
    name = models.CharField(max_length=300,blank=True,null=True)
    price = models.FloatField()
    avail = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    in_offer = models.BooleanField(default=False)
    offer_percentage = models.IntegerField(default=0)
    category = models.CharField(max_length=20,choices=WEBURLS,null=True,blank=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete =  models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=300,null=True)
    ordertotal = models.FloatField(blank=True,null=True)
    acceptorder = models.BooleanField(default=False,blank=True,null=True)
    declineorder = models.BooleanField(default=False,blank=True,null=True)
    def __str__(self):
        return str(self.id)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.avail == False:
                shipping = True
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
        return orderitems

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=11,decimal_places=2,blank=True,null=True)
    total_price = models.DecimalField(max_digits=11,decimal_places=2,blank=True,null=True)    
    def __str__(self):
        return str(self.order)
    @property
    def get_total(self):
        if self.product.in_offer:
            total = (self.product.price -(self.product.price*self.product.offer_percentage)/100) * self.quantity
        else:
            total = self.product.price * self.quantity
        return total

class WishListItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    phone = models.CharField(blank=True,null=True,max_length=10,default=0)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    state = models.CharField(max_length=300,blank=True,null=True)
    zipcode = models.CharField(max_length=300,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.customer)
