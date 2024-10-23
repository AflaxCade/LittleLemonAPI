from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('menu-items', views.menu_items, name='menu_items'),
    path('menu-items/<int:pk>', views.single_items, name='single_items'),
    path('cart/menu-items', views.cart_menu_items, name='cart_menu_items'),
    path('groups/manager/users', views.managers, name='managers'),
    path('orders', views.orders, name='orders'),
    path('orders/<int:pk>', views.single_order, name='single_order'),
    path('groups/manager/users/<int:pk>', views.single_manager, name='managers'),
    path('groups/delivery-crew/users', views.delivery_crew, name='delivery_crew'),
    path('groups/delivery-crew/users/<int:pk>', views.single_delivery_crew, name='delivery_crew'),
]