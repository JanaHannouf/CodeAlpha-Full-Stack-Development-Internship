from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from core.models import Category, Product, ProductImages, ProductReview, Address, Wishlist, CartOrderItems, CartOrder, Subscribe
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from userauths.models import Profile, ContactUs

# Create your views here.
def index(request):
    products = Product.objects.filter(featured=True, in_stock=True)

    context = {
        "products" : products,
    }
    return render(request, 'core/index.html', context)

def about_us(request):
    return render(request, 'core/about-us.html')

def category_products(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(in_stock=True, category=category)

    context = {
        "category" : category,
        "products" : products
    }
    return render(request, 'core/category-products.html', context)

def help(request):
    return render(request, 'core/help.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def product_details(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = product.product_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        'product' : product,
        'product_images' : product_images,
        'products' : products,
        'reviews' : reviews,
        'average_rating' : average_rating,
        'review_form' : review_form,
        'make_review' : make_review,
        'profile' : profile
    }
    return render(request, 'core/product-details.html', context)

def returns(request):
    return render(request, 'core/returns.html')

def search_results(request):
    query = request.GET['search']

    products = Product.objects.filter(title__icontains=query).order_by("-pid")

    context = {
        "products" : products,
        "query" : query
    }
    return render(request, 'core/search-results.html', context)

def shipping(request):
    return render(request, 'core/shipping.html')

def shop(request):
    products = Product.objects.filter(in_stock=True)

    context = {
        "products" : products,
    }
    return render(request, 'core/shop.html', context)

def terms(request):
    return render(request, 'core/terms.html')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by("-date")
   
    context = {
        "wishlist_items" : wishlist_items
    }

    return render(request, 'core/wishlist.html', context)

def tag(request, tag_slug=None):
    products = Product.objects.filter(in_stock=True)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products" : products,
        "tag" : tag
    }
    return render(request, "core/tag.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating']
    )

    context = {
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool' : True,
            'context' : context,
            'average_reviews' : average_reviews
        }
    )

def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj'])})

def cart(request):
    cart_total_amount = 0
    
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = float(item['price']) if item['price'] else 0.0
            cart_total_amount += int(item['qty']) * price
        return render(request, 'core/cart.html', {"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty.")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount}) 
    return JsonResponse({"data": context, 'totalCartItems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount}) 
    return JsonResponse({"data": context, 'totalCartItems': len(request.session['cart_data_obj'])})


@login_required    
def checkout(request):
    profile = Profile.objects.get(user=request.user)
    order_id = None
    cart_total_amount = 0
    total_amount = 0
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])

            order = CartOrder.objects.create(
                user = request.user,
                full_name = full_name,
                email = email,
                phone_number = phone_number,
                address = address,
                payment_method = payment_method,
                price = total_amount,
            )
            order_id = order.id

            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
                cart_order_items = CartOrderItems.objects.create(
                    order = order,
                    invoice_number = "INVOICE_NUMBER" + str(order.id),
                    item = item['title'],
                    image = item['image'],
                    quantity = item['qty'],
                    price = item['price'],
                    total = float(item['qty']) * float(item['price'])
                )

        return redirect("core:confirmation", order_id=order_id)

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple addresses, only one should be activated.")
        active_address = None

    return render(request, 'core/checkout.html', 
        {
            "cart_data": request.session['cart_data_obj'], 
            'totalCartItems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount, 
            'active_address': active_address,
            'profile' : profile
        }
    )   

@login_required
def confirmation(request, order_id):
    order = CartOrder.objects.get(id=order_id)
    order_items = CartOrderItems.objects.filter(order=order)

    cart_total_amount = sum(item.total for item in order_items)

    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']

    totalCartItems = 0

    context = {
        'order': order,
        'order_items': order_items,
        'totalCartItems': len(order_items),
        'cart_total_amount': cart_total_amount,
        'totalCartItems': totalCartItems
    }

    return render(request, 'core/confirmation.html', context)

@login_required
def account(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    addresses = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        new_address = Address.objects.create(
            user=request.user,  
            address=address,
            phone_number=phone
        )
        messages.success(request, "Address added successfully.")
        return redirect("core:account")

    context = {
        "orders": orders,
        "address": addresses,
        'profile' : profile,
        'wishlist' : wishlist
    }
    return render(request, 'core/account.html', context)

def order_details(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    items = CartOrderItems.objects.filter(order=order)

    context = {
        "order" : order,
        'items' : items
    }
    return render(request, 'core/order-details.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()

    if wishlist_count > 0:
        context = {
            "bool" : True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user = request.user,
            product = product
        )
        context = {
            "bool" : True
        }

    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    product = Wishlist.objects.get(id=pid)
    product.delete()

    context = {
        "bool" : True,
        "wishlist" : wishlist,
    }
    wishlist__json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data":data, "wishlist_items": wishlist__json})

def contact(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        "profile" : profile
    }
    return render(request, 'core/contact.html', context)

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        subject = subject,
        message = message
    )

    context = {
        "bool" : True,
    }
    return JsonResponse({"data":context})

def ajax_subscribe_newsletter(request):
    email = request.GET['email']

    new_subscribe = Subscribe.objects.create(
        email = email
    )

    context = {
        "bool" : True,
    }
    return JsonResponse({"data":context})