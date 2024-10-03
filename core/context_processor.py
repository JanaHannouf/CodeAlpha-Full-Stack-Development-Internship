from core.models import Category, Product, ProductImages, ProductReview, Address, Wishlist, CartOrderItems, CartOrder
from django.contrib import messages

def default(request):
    categories = Category.objects.all()

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        wishlist = None

    return {
        'categories' : categories,
        'address' : address,
        'wishlist' : wishlist
    }