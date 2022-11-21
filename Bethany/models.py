from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    images = models.URLField(max_length=255)

    def __str__(self):
        return self.title


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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=240)
    email = models.CharField(max_length=240, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
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
    email = models.EmailField(max_length=30)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=10)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email','address','phone','image']
