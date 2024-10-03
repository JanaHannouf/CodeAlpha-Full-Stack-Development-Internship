from django.contrib import admin
from core.models import Category, Product, ProductImages, ProductReview, Address, Wishlist, CartOrderItems, CartOrder, Subscribe

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'product_image', 'price', 'category', 'featured', 'in_stock']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'order_status']
    list_display = ['user', 'full_name', 'email', 'phone_number', 'address', 'payment_method','price', 'paid_status', 'order_date', 'order_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'item', 'image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating', 'date']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'phone_number', 'status']

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Subscribe, SubscribeAdmin)