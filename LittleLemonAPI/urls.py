from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menu_items, name='menu_items'),
    path('menu-items/<int:pk>', views.single_items, name='single_items'),
    path('groups/manager/users', views.managers, name='managers'),
    path('groups/manager/users/<int:pk>', views.single_manager, name='managers'),
]