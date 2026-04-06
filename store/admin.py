from django.contrib import admin
from .models import Product, Cart, Order, OrderItem
from .models import Blog

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'payment_method')
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Blog)