from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["id"]

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "featured", "category")
    list_filter = ("featured", "category")
    search_fields = ("title", "category")
    ordering = ["id"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
