from django.db import models
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
    
    
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
# class Basket(models.Model):
#             user = models.ForeignKey(User, on_delete=models.CASCADE)
#             product = models.ForeignKey(Product, on_delete=models.CASCADE)
#             quantity=models.IntegerField()
#             pass
#             def __str__(self):
#                     return self.title


# class Oreder(models.Model):

#             order_number=models.IntegerField()
#             products = models.ManyToManyField(Basket)
#             ordered = models.BooleanField(default=False)
#             user = models.ForeignKey(User, on_delete=models.CASCADE)
#             start_date = models.DateTimeField(auto_now_add=True)
#             oredered_date=models.DateTimeField()
#             user_discount=models.DecimalField()
#             total_price=models.IntegerField()
#             def __str__(self):
#                     return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name
class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  f"{self.item}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    print(user.name)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.user)





# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     state = models.CharField(max_length=200, null=False)
#     zipcode = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address


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

