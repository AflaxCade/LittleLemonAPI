from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem
from .serializers import MenuItemSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
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
@permission_classes([IsAuthenticated])
def single_items(request, pk):
    items = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'GET':
        serializer = MenuItemSerializer(items)
        return Response(serializer.data)
    
    # Check if user is a manager or superuser once for PUT/DELETE
    is_manager = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
    
    if request.method == 'PUT':
        if is_manager:
            serializer = MenuItemSerializer(items, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        if is_manager:
            items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)