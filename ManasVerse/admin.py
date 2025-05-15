from django.contrib import admin
from .models import Product, Category, Order, OrderItem

# CategoryAdmin for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Display the id and name fields for Category in the admin list

# ProductAdmin for Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price']  # Display the id, name, category, and price for Product in the admin list
    prepopulated_fields = {'slug': ('name',)}  # Automatically generate the slug field from the name field

# OrderItemInline to display items in an order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms will be displayed

# OrderAdmin for Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'total_amount', 'created_at', 'status')  # Add 'status' to the displayed columns
    list_filter = ('status', 'created_at')  # Allow filtering by status and created_at date
    search_fields = ('name', 'email', 'phone')  # Enable search functionality for name, email, and phone fields
    inlines = [OrderItemInline]  # Display order items inline within the order in the admin panel
