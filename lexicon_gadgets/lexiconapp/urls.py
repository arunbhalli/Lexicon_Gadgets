from django.conf import settings
from django.conf.urls.static import static
from lexiconapp import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='base'),
    path('adminpage/orders/', views.ordersall, name='adminpageorders'),
    path('logout/', views.userlogout, name='userlogout'),
    path('card', views.card, name='card'),
    path('lexiconapp/add/', views.add, name='add'),
    path('lexiconapp/add/addrecord/', views.addrecord, name='addrecord'),
    path('lexiconapp/delete/<int:id>', views.delete, name='delete'),
    path('lexiconapp/update/<int:id>', views.update, name='update'),
    path('lexiconapp/update/updaterecord/<int:id>',
         views.updaterecord, name='updaterecord'),
    path("signup", views.signup, name='signup'),
    path('orders/', views.orderbyuser, name='orders'),
    path('contact/', views.contact, name='contact'),
    path('adminpage/contact/', views.contactall, name='adminpagecontact'),
    path('profile/', views.profile, name='profile'),
    path('adminpage/profile/', views.profileall, name='adminpageprofile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('search/', views.search, name='search'),
    path('adminpage/', views.adminpage, name='adminpage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
