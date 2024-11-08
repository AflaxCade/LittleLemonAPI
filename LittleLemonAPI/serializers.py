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


class CartHelpSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['id','title','price']


class CartSerializer(serializers.ModelSerializer):
    menuitems = CartHelpSerializer(read_only=True)
    menuitems_id = serializers.IntegerField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitems', 'menuitems_id', 'quantity', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem =  serializers.SlugRelatedField(slug_field='title', queryset=MenuItem.objects.all(), read_only=False)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)


    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'orderitem_set']