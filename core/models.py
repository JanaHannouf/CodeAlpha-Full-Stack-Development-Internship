from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

ORDER_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered")
)

PAYMENT_CHOICE = (
    ("cash on delivery", "Cash on Delivery"),
    ("credit card", "Credit Card"),
    ("paypal", "PayPal")
)

RATING_CHOICE = (
    ( 1, "✭☆☆☆☆"),
    ( 2, "✭✭☆☆☆"),
    ( 3, "✭✭✭☆☆"),
    ( 4, "✭✭✭✭☆"),
    ( 5, "✭✭✭✭✭"),
)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Category Title")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prod", alphabet="abcdefgh12345")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")

    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to="product", default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")

    tags = TaggableManager(blank=True)

    in_stock = models.BooleanField(default=True)
    stock_count = models.IntegerField(default=10, null=True, blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        percentage = (self.price / self.old_price) * 100
        return int(percentage)

    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")

    class Meta:
        verbose_name_plural = "Product Images"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENT_CHOICE, max_length=30)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_CHOICE, max_length=20, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def item_image(self):
        return mark_safe('img< src="%s" width="50" height="50" />' % (self.image))
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICE, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

class Subscribe(models.Model):
    email = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Subscribes"