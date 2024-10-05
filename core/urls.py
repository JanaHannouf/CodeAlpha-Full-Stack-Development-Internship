from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),  # Root URL for the homepag
    path('about-us/', about_us, name='about_us'),  # URL for the about-us page
    path('account/', account, name='account'),  # URL for the account management page
    path('account/order-history/', order_history, name='order-history'),  # URL for the order history page
    path('account/wishlist/', account_wishlist, name='account-wishlist'),  # URL for the account wishlist page
    path('account/address-book/', address_book, name='address-book'),  # URL for the address book page
    path('account/settings/', account_settings, name='account-settings'),  # URL for the account settings page
    path('cart/', cart, name='cart'),  # URL for the cart page
    path('category-products/<cid>/', category_products, name='category_products'),  # URL for the products represented based on category page
    path('checkout/', checkout, name='checkout'),  # URL for the checkout page
    path('confirmation/<int:order_id>/', confirmation, name='confirmation'),  # URL for the confirmation page
    path('contact/', contact, name='contact'),  # URL for the contact us page
    path('help/', help, name='help'),  # URL for the help center page
    path('account/order-details/<int:id>/', order_details, name='order_details'),  # URL for the order details page
    path('privacy/', privacy, name='privacy'),  # URL for the privacy policy page
    path('product-details/<str:pid>/', product_details, name='product_details'),  # URL for the product details page
    path('returns/', returns, name='returns'),  # URL for the returns & exhanges page
    path('search-results/', search_results, name='search_results'),  # URL for the search results page
    path('shipping/', shipping, name='shipping'),  # URL for the shipping information page
    path('shop/', shop, name='shop'),  # URL for the shop now page
    path('terms/', terms, name='terms'),  # URL for the terms & conditions page
    path('wishlist/', wishlist, name='wishlist'),  # URL for the wishlist page
    path('products/tag/<slug:tag_slug>/', tag, name='tags'),  # URL for the tag page
    path('ajax-add-review/<pid>/', ajax_add_review, name='ajax_add_review'), # URL for adding review
    path('add-to-cart/', add_to_cart, name='add_to_cart'), # URL for adding items to cart
    path('delete-from-cart/', delete_item_from_cart, name='delete-from-cart'), # Delete item from cart URL
    path('update-cart/', update_cart, name='update-cart'), # Delete item from cart URL
    path('make-default-address/', make_default_address, name="make-default-address"), # Make Default Address URL
    path('add-to-wishlist/', add_to_wishlist, name="add-to-wishlist"), # Add to wishlist URL
    path('remove-from-wishlist/', remove_wishlist, name='remove-from-wishlist'), # Remove from wishlist URL
    path('ajax-contact-form/', ajax_contact_form, name="ajax-contact-form"), # Ajax for contact us form URL
    path('ajax-subscribe-form/', ajax_subscribe_newsletter, name='ajax-subscribe-form'), # Subscribtion URL
]