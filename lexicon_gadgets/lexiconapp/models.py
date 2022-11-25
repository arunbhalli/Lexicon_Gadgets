from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import slugify 
from django.shortcuts import reverse
# Create your models here.
CATEGORIES = (
        ('CO','Computers'),
        ('HA','Home Aplliances'),
        ('MS','Mobiles & Smartwatch'),
        ('S','Sound')
    )

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES,max_length=255)
    images = models.URLField(max_length=255)
    slug = models.SlugField()
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product-view", kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
         return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })
         
    def get_remove_from_cart_url(self):
         return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })  
             

       
        
    
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.customer} and transactionid {self.transaction_id}"



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
          return  f"{self.product} and quantity {self.quantity}"
    def get_total_item_price(self):
        return self.quantity*self.product.price
    def get_final_price(self):
        item_price=self.get_total_item_price
        return item_price 
    @property
    def get_total(self):
          total = 0
          for order_item in self.product.all():
             total += order_item.get_total_item_price() 
          return total,print(total)
    
    # def get_total(self):
    #       total = 0
    #       for i in range(self.quantity):
    #          total += int(self.get_total_item_price())
    #       return total
    
class BasketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    complete = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  f"{self.item}"
    def get_total_item_price(self):
        return self.quantity*self.item.price
    def get_final_price(self):
        item_price=self.get_total_item_price
        return item_price

class BasketOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(BasketItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.user)
    @property
    def get_total(self):
          total = 0
          for order_item in self.items.all():
             total += order_item.get_total_item_price() 
          return total




class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=10)
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        # return self.name
        return " Message from " + self.name + ' - ' + self.email

# user profile_pics


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=10)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address','image']

class UserUpdateForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ['email']



class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
