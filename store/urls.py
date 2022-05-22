from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('account/login', login_view, name='login'),
    path('account/register', register_view, name='register'),
    path('account/logout', logout_view, name='logout'),
    path('cart',cart_view, name='cart'),
    path('checkout', checkout_view, name='checkout'),
    path('payment/', payment_view, name='payment'),
    path('search/', search_view, name='search'),
    path('process_order/', processOrder, name='process_order'),
    path('update_item/', updateItem_view, name='update_item'),
    path('product-detail/<str:pk>/', product_detail_view, name='product-detail'),
    path('category-product/<str:pk>/', category_product_view, name='category'),
    path('category-product/all', all_product_view, name='all-product'),
    path('blog', blog_view, name='blog'),
    path('blog-detail/<str:pk>/', blog_detail_view, name='blog-detail'),
    path('contact-us', contact_us_view, name='contact-us'),




]
