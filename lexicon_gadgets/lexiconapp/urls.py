from django.conf import settings
from django.conf.urls.static import static
from lexiconapp import views
from .views import *
from django.urls import path
from .views import CheckoutView


from django.urls import path
urlpatterns = [
    path('', views.index, name='base'),
    path('orderall/', views.orderall, name='orderall'),
    path('logout/', views.userlogout, name='userlogout'),
    path("card1/<str:slug>", ItemDetailView.as_view(), name='product-view'),
    path("card1/add-to-cart/<str:slug>", views.add_to_cart, name='add-to-cart'),
    path("card1/remove-item-from-cart/<str:slug>",
         views.remove_from_cart, name='remove-from-cart'),
    path("card1/remove-single-item-from-cart/<str:slug>",
         views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('card/', views.card, name='card'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('lexiconapp/add/', views.add, name='add'),
    path('lexiconapp/add/addrecord/', views.addrecord, name='addrecord'),
    path('lexiconapp/delete/<str:slug>', views.delete, name='delete'),
    path('lexiconapp/update/<str:slug>', views.update, name='update'),
    path('lexiconapp/update/updaterecord/<int:id>',
         views.updaterecord, name='updaterecord'),
    path("signup", views.signup, name='signup'),
    path('orders/', views.orderbyuser, name='orders'),
    path('contact/', views.contact, name='contact'),
    path('contactall/', views.contactall, name='contactall'),
    path('profile/', views.profile, name='profile'),
    path('profileall/', views.profileall, name='profileall'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
