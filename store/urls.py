from django.urls import path
from . import views

urlpatterns = [
    # ========================
    # Product-related URLs
    # ========================
    path('', views.product_list, name='product_list'),  # Display all products on the homepage
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  # Product details page
    path('products/category/<str:category>/', views.product_category, name='product_category'),  # Filter products by category
    path('products/search/', views.product_search, name='product_search'),  # Search products by name or description
    
    # ========================
    # Cart and Checkout URLs
    # ========================
    path('cart/', views.cart_view, name='cart'),  # View items in the cart
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove product from cart
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),  # Update product quantity in cart
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    
    # ========================
    # Order-related URLs
    # ========================
    path('orders/', views.order_list, name='order_list'),  # View user orders
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),  # View specific order details
    path('orders/history/', views.order_history, name='order_history'),  # View order history for logged-in users
    
    # ========================
    # Authentication URLs
    # ========================
    path('account/login/', views.user_login, name='login'),  # User login page
    path('account/register/', views.user_register, name='register'),  # User registration page
    path('account/logout/', views.user_logout, name='logout'),  # User logout page

    # ========================
    # User-related URLs
    # ========================
    path('account/profile/', views.user_profile, name='profile'),  # User profile page
    path('account/edit-profile/', views.edit_profile, name='edit_profile'),  # Edit user profile details
    path('account/change-password/', views.change_password, name='change_password'),  # Change password for logged-in users
    
    # ========================
    # Home and Static Pages
    # ========================
    path('home/', views.home, name='home'),  # Home page (if separate from product list)
    path('contact/', views.contact, name='contact'),  # Contact page
    path('about/', views.about, name='about'),  # About page
    path('faq/', views.faq, name='faq'),  # FAQ page
    path('terms-and-conditions/', views.terms, name='terms'),  # Terms and conditions page
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy policy page
    
    # ========================
    # Admin and Management URLs (Optional)
    # ========================
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard page
    path('admin/products/', views.admin_product_list, name='admin_product_list'),  # Admin product management
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),  # Admin order management
]
