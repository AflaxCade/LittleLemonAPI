from django.db.models import Prefetch
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer,OrderItemSerializer, OrderSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        perpage = request.query_params.get('perpage', default=10)
        page = request.query_params.get('page', default=1)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def single_items(request, pk):
    items = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'GET':
        serializer = MenuItemSerializer(items)
        return Response(serializer.data)
    
    is_manager_or_superuser = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
    
    if request.method == 'PUT':
        if is_manager_or_superuser:
            serializer = MenuItemSerializer(items, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        if is_manager_or_superuser:
            items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'POST'])   
@permission_classes([IsAuthenticated])
def managers(request):
    is_manager_or_superuser = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    if request.method == 'GET':
        if is_manager_or_superuser:
            users = User.objects.filter(groups__name='Manager')
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        if is_manager_or_superuser:
            user_id = request.data.get('id')
            if not user_id:
                return Response({"detail": "User ID required"}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=user_id) if user_id else get_object_or_404(User, username=user_name)
            if user.groups.filter(name='Manager').exists():
                return Response({"detail": "User already in manager group"}, status=status.HTTP_400_BAD_REQUEST)
            manager_group = Group.objects.get(name='Manager')
            user.groups.add(manager_group)
            return Response({"detail": "User added to manager group"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'DELETE'])   
@permission_classes([IsAuthenticated])
def single_manager(request, pk):
    user = get_object_or_404(User, id=pk)
    is_manager_or_superuser = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    if request.method == 'GET':
        if is_manager_or_superuser:
            if not user.groups.filter(name='Manager').exists():
                return Response({"detail": "User not in manager group"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        if is_manager_or_superuser:
            if user.groups.filter(name='Manager').exists():
                manager_group = Group.objects.get(name='Manager')
                user.groups.remove(manager_group)
                return Response({"detail": "User removed from manager group"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "User not in manager group"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'POST'])   
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    is_manager_or_superuser = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    if request.method == 'GET':
        if is_manager_or_superuser:
            users = User.objects.filter(groups__name='Delivery Crew')
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        if is_manager_or_superuser:
            user_id = request.data.get('id')
            if not user_id:
                return Response({"detail": "User ID required"}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=user_id) if user_id else get_object_or_404(User, username=user_name)
            if user.groups.filter(name='Delivery Crew').exists():
                return Response({"detail": "User already in delivery crew group"}, status=status.HTTP_400_BAD_REQUEST)
            delivery_crew_group = Group.objects.get(name='Delivery Crew')
            user.groups.add(delivery_crew_group)
            return Response({"detail": "User added to delivery crew group"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'DELETE'])   
@permission_classes([IsAuthenticated])
def single_delivery_crew(request, pk):
    user = get_object_or_404(User, id=pk)
    is_manager_or_superuser = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    if request.method == 'GET':
        if is_manager_or_superuser:
            if not user.groups.filter(name='Delivery Crew').exists():
                return Response({"detail": "User not in delivery crew group"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        if is_manager_or_superuser:
            if user.groups.filter(name='Delivery Crew').exists():
                delivery_crew_group = Group.objects.get(name='Delivery Crew')
                user.groups.remove(delivery_crew_group)
                return Response({"detail": "User removed from delivery crew group"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "User not in delivery crew group"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_menu_items(request):
    user = request.user

    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        return Response({"detail": "Managers and Superusers are not allowed to access this endpoint."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        cart_items = Cart.objects.select_related('menuitems').filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        menuitem_id = request.data.get('menuitems_id')
        menuitem = get_object_or_404(MenuItem, id=menuitem_id)

        if Cart.objects.filter(user=user, menuitems=menuitem).exists():
            return Response({"detail": "Item already in cart"}, status=status.HTTP_400_BAD_REQUEST)
        quantity = int(request.data.get('quantity', 1))
        if quantity < 1:
            return Response({"detail": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)
        unit_price = round(menuitem.price, 2)
        total_price = round(unit_price * quantity, 2)

        serializer = CartSerializer(data={
            'menuitems_id': menuitem.id,
            'quantity': quantity,
            'unit_price': unit_price,
            'price': total_price
        })
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"detail": "Cart is already empty"}, status=status.HTTP_404_NOT_FOUND)
        cart_items.delete()
        return Response({"detail": "All cart items delcleraed successfully"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    user = request.user
    perpage = request.query_params.get('perpage', default=10)
    page = request.query_params.get('page', default=1)

    if request.method == 'GET':
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            # Managers: Return all orders
            orders = Order.objects.prefetch_related(
                Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('menuitem'))).all()
            
            order_status = request.query_params.get('status')
            if order_status == 'delivered':
                orders = orders.filter(status=True)
            elif order_status == 'pending':
                orders = orders.filter(status=False)
        elif user.groups.filter(name='Delivery Crew').exists():
            # Delivery crew: Return all orders assigned to this crew member
            orders = Order.objects.prefetch_related(
                Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('menuitem'))
                ).filter(delivery_crew=user, status=False)
        else:
            # Customers: Return orders created by this user
            orders = Order.objects.prefetch_related(
            Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('menuitem'))).filter(user=user)

        # Apply pagination to the orders
        paginator = Paginator(orders, per_page=perpage)
        try:
            orders = paginator.page(number=page)
        except EmptyPage:
            orders = []
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        if not user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists() and not user.is_superuser:
            # Get the cart items for this user
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new order for the user
            order = Order.objects.create(user=user, total=0)

            total_price = 0
            # Create order items from the cart items
            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitems,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price
                )
                total_price += order_item.price

            # Update the total price of the order
            order.total = total_price
            order.save()

            # Clear the cart after creating the order
            cart_items.delete()

            return Response({"detail": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request, pk):
    user = request.user
    order = get_object_or_404(
    Order.objects.prefetch_related('orderitem_set__menuitem').select_related('user', 'delivery_crew'), pk=pk)
    # Check if the user is allowed to access this order
    if request.method == 'GET':
        # Customers: Only access their own orders
        if not user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists() and not user.is_superuser:
            if order.user != user:
                return Response({"detail": "Not authorized to view this order"}, status=status.HTTP_403_FORBIDDEN)
        # Delivery Crew: Only access orders assigned to them
        elif user.groups.filter(name='Delivery Crew').exists():
            if order.delivery_crew != user:
                return Response({"detail": "Not authorized to view this order"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            # Managers: Can update delivery crew and status
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.groups.filter(name='Delivery Crew').exists():
            # Delivery Crew: Can only update order status
            if 'status' not in request.data:
                return Response({"detail": "Only status can be updated by delivery crew"}, status=status.HTTP_400_BAD_REQUEST)
            order.status = request.data['status']
            order.save()
            return Response({"detail": "Order status updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            # Managers can delete orders
            order.delete()
            return Response({"detail": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    