from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from lexiconapp.models import *
from lexiconapp import forms
from django.contrib.auth.forms import UserChangeForm
from .models import ProfileUpdateForm, UserUpdateForm, CheckoutAddress
from django.urls import reverse
from django.views.generic import View, DetailView
from django.template import loader
from django.utils.crypto import get_random_string
# Create your views here.


def check_admin(user):
    # print(user.is_superuser)
    return user.is_superuser


def error_404_view(request, exception):
    return redirect('userlogin')


def index(request):
    return render(request, 'lexiconapp/base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.error(
                request, "Password does not Match,Please Try Again!")
            return redirect('/signup')
        try:
            if User.objects.get(username=username):
                messages.warning(request, "Username Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass
        # checks for error inputs
        user = User.objects.create_user(username, email, pass1)
        user.save()
        customer = Customer(user=user, name=username)
        customer.save()
        messages.info(request, 'Thanks For Signing Up')
        # messages.info(request,"Signup Successful Please Login")
        return redirect('/login')
    return render(request, "lexiconapp/signup.html")


def userlogin(request):

    if request.method == 'POST':
        login_form = forms.UserLogin(data=request.POST)

        myusername = request.POST['username']
        mypassword = request.POST['password']

        user = authenticate(username=myusername, password=mypassword)
        print(user)
        # user = not None
        if user is not None:
            login(request, user)
            return render(request, 'lexiconapp/login.html', {'user': user})
        else:
            print("error")

    else:
        login_form = forms.UserLogin()

    return render(request, 'lexiconapp/login.html', {'login_form': login_form})


@user_passes_test(check_admin,login_url='/login')
def ordersall(request):
    customer = Customer.objects.all()
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    shippingaddress = ShippingAddress.objects.all()

    context = {
        'customer': customer,
        'orders': orders,
        'orderitems': orderitems,
        'shippingaddress': shippingaddress,
    }
    return render(request, 'lexiconapp/orderall.html', context)


@login_required
def orderbyuser(request):
    customer = Customer.objects.get(name=request.user)
    orders = Order.objects.filter(customer=customer)
    orderitems = OrderItem.objects.filter(order__in=orders)
    shippingaddress = ShippingAddress.objects.filter(order__in=orders)

    context = {
        'orders': orders,
        'orderitems': orderitems,
        'shippingaddress': shippingaddress,
    }
    return render(request, 'lexiconapp/orders.html', context)


@login_required
def userlogout(request):
    logout(request)
    messages.success(request, 'logged out success')
    return redirect('userlogin')


def card(request):
    item_list = Product.objects.all().values()
    context = {'items': item_list, }
    return render(request, 'lexiconapp/card.html', context)


@user_passes_test(check_admin, login_url='/login')
def add(request):
    template = loader.get_template('lexiconapp/add.html')
    return HttpResponse(template.render({}, request))


@user_passes_test(check_admin, login_url='/login')
def addrecord(request):
    a = request.POST.get('Title', False)
    d = request.POST.get('Description', False)
    e = request.POST.get('Price', False)
    b = request.POST.get('Brand', False)
    f = request.POST.get('Category', False)
    c = request.POST.get('Images', False)
    product = Product(title=a, description=d, price=e,
                      brand=b, category=f, images=c)
    product.save()
    return HttpResponseRedirect(reverse('card'))

# update record


@user_passes_test(check_admin, login_url='/login')
def updaterecord(request, id):
    a = request.POST.get('Title', False)
    d = request.POST.get('Description', False)
    e = request.POST.get('Price', False)
    b = request.POST.get('Brand', False)
    f = request.POST.get('Category', False)
    c = request.POST.get('Images', False)
    product = Product.objects.get(id=id)
    product.title = a
    product.description = d
    product.price = e
    product.brand = b
    product.category = f
    product.images = c
    product.save()
    return HttpResponseRedirect(reverse('card'))


@user_passes_test(check_admin, login_url='/login')
def delete(request, slug):
    product = Product.objects.get(slug=slug)
    product.delete()
    return HttpResponseRedirect(reverse('card'))


@user_passes_test(check_admin, login_url='/login')
def update(request, slug):
    selected_product = Product.objects.get(slug=slug)
    template = loader.get_template('lexiconapp/update.html')
    context = {
        'item': selected_product,
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # if len(name) > 4 and len(phone) > 8 and len(message) > 2:
        #     messages.error(request, "Please fill the form correctly")
        # else:
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.message = message
        contact.save()
        messages.success(request, "Your message has been successfully sent")
    return render(request, 'lexiconapp/contact.html')


@user_passes_test(check_admin, login_url='/login')
def contactall(request):

    contacts = Contact.objects.all()

    context = {
        'contacts': contacts,
    }
    return render(request, 'lexiconapp/contactall.html', context)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'lexiconapp/profile.html', context)


@user_passes_test(check_admin, login_url='/login')
def profileall(request):

    p_form = ProfileUpdateForm.Meta.fields
    users = User.objects.all()

    context = {
        'p_form': p_form,
        'users': users,
    }

    return render(request, 'lexiconapp/profileall.html', context)


@login_required(login_url='login')
def updateprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'lexiconapp/updateprofile.html', context)
    # Redirect back to profile page
# search functionality


def search(request):
    query = request.GET.get('query')
    item_list = Product.objects.filter(title__icontains=query)
    params = {'items': item_list, }
    return render(request, 'lexiconapp/card.html', params)


class ItemDetailView(DetailView):
    model = Product
    template_name = "lexiconapp/product.html"

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = BasketItem.objects.get_or_create(
        item=item,
        user=request.user,
        complete=False
    )
    order_qs = BasketOrder.objects.filter(user=request.user, complete=False)
    if order_qs:
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            order_item.quantity += 1
            print(order_item.quantity)
            order_item.save()
            messages.info(
                request, "This item quantity was updated successfully")
            return redirect('order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, "This item  was added to your basket")
            return redirect('product-view', slug=slug)
    else:
        order = BasketOrder.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item  was added to your basket")
        return redirect('product-view', slug=slug)
    return redirect('product-view', slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = BasketOrder.objects.filter(user=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = BasketItem.objects.filter(
                item=item,
                user=request.user,
                complete=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product-view', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('product-view', slug=slug)
    return redirect('product-view', slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = BasketOrder.objects.filter(user=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = BasketItem.objects.filter(
                item=item,
                user=request.user,
                complete=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item) 
            messages.info(request, "This item quantity was updated.")              
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product-view', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('product-view', slug=slug)

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = BasketOrder.objects.get(user=self.request.user, complete=False)
            context = {
                'object': order
            }
            return render(self.request, 'lexiconapp/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('card')
       

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'lexiconapp/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = BasketOrder.objects.get(user=self.request.user, complete=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                return redirect('conforder')
            messages.warning(self.request, "Failed Checkout")
            return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("order-summary")

@login_required
def conforder(request):
    basketorders = BasketOrder.objects.filter(user=request.user)
    basketitems = BasketItem.objects.filter(user=request.user)
    checkoutaddress = CheckoutAddress.objects.filter(user=request.user)
    customer = Customer.objects.get(name=request.user)
    product = []
    quantity = []
    transaction_id = get_random_string(length=32)
    
    # for basketorder in basketorders:
    #     user = basketorder.user
    #     orderitems = basketorder.items
    #     date_ordered = basketorder.date_ordered
    #     print(basketorder)

    for address in checkoutaddress:
        street_address = address.street_address
        apartment_address = address.apartment_address
        country = address.country
        zip = address.zip


    count=0
    for basketitem in basketitems:
        
        product.insert(count,basketitem.item)
        quantity.insert(count,basketitem.quantity)
        count=+1
    
    
    
    order = Order()
    order.customer = customer
    # order.date_ordered = date_ordered
    order.complete = True
    order.transaction_id = transaction_id
    order.save()
    
    shipping = ShippingAddress()
    shipping.customer = customer
    shipping.order = order
    shipping.address = street_address
    shipping.city = apartment_address
    shipping.state = country
    shipping.zipcode = zip
    shipping.save()

    
    count= 0
    for i in range(len(product)):
        if count <= len(product):
            orderitem = OrderItem()
            orderitem.order = order
            orderitem.product = product[i]
            orderitem.quantity = quantity[i]
            orderitem.save()


    
     

    basketorders.delete()
    basketitems.delete()
    checkoutaddress.delete()

    print(product,quantity)
    print(transaction_id)
    return redirect('userlogin')

 
def adminpage(request):
    
    return render(request, 'lexiconapp/adminpage.html')
