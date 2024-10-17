from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField(method_name='get_Date_Joined')
    class Meta:
        model = User
        fields = ['id', 'username', 'email','date_joined']
    
    def get_Date_Joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')