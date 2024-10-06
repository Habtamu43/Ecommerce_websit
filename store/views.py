from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order, Cart, OrderItem  # Assuming these models are defined
from .forms import RegistrationForm, LoginForm, ProfileForm, CheckoutForm  # Assuming these forms are defined

# ========================
# Product-related Views
# ========================

def product_list(request):
    """View to list all products on the homepage."""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    """View to display a single product's details."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def product_category(request, category):
    """View to filter products by category."""
    products = Product.objects.filter(category__iexact=category)
    return render(request, 'store/product_list.html', {'products': products, 'category': category})

def product_search(request):
    """View to search products by name or description."""
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'query': query})

# ========================
# Cart and Checkout Views
# ========================

@login_required
def cart_view(request):
    """View to display the current user's cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product)
    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.remove_product(product)
    messages.success(request, f'{product.name} has been removed from your cart.')
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    """Update product quantity in the cart."""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart.objects.get(user=request.user)
    cart.update_product(product, quantity)
    messages.success(request, f'{product.name} quantity updated to {quantity}.')
    return redirect('cart')

@login_required
def checkout(request):
    """Checkout view to handle user purchases."""
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            cart.clear()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('order_list')
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

# ========================
# Order-related Views
# ========================

@login_required
def order_list(request):
    """View to display the current user's orders."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View to display details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def order_history(request):
    """View to display the user's order history."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

# ========================
# Authentication Views
# ========================

def user_login(request):
    """User login view."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def user_register(request):
    """User registration view."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def user_logout(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# ========================
# User-related Views
# ========================

@login_required
def user_profile(request):
    """User profile view."""
    return render(request, 'store/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    """Edit user profile view."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'store/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    """Change password view."""
    # Implement password change logic using Django's built-in forms or custom form.
    return render(request, 'store/change_password.html')

# ========================
# Home and Static Pages
# ========================

def home(request):
    """Home view, can be used to display featured products or promotions."""
    products = Product.objects.all()[:8]  # Display first 8 products as featured.
    return render(request, 'store/home.html', {'products': products})

def contact(request):
    """Contact page view."""
    return render(request, 'store/contact.html')

def about(request):
    """About page view."""
    return render(request, 'store/about.html')

def faq(request):
    """FAQ page view."""
    return render(request, 'store/faq.html')

def terms(request):
    """Terms and conditions page view."""
    return render(request, 'store/terms.html')

def privacy_policy(request):
    """Privacy policy page view."""
    return render(request, 'store/privacy_policy.html')

# ========================
# Admin and Management Views (Optional)
# ========================

@login_required
def admin_dashboard(request):
    """Admin dashboard view for monitoring the store's performance."""
    # Display key metrics like total orders, revenue, etc.
    return render(request, 'store/admin_dashboard.html')

@login_required
def admin_product_list(request):
    """Admin view to manage products."""
    products = Product.objects.all()
    return render(request, 'store/admin_product_list.html', {'products': products})

@login_required
def admin_order_list(request):
    """Admin view to manage orders."""
    orders = Order.objects.all()
    return render(request, 'store/admin_order_list.html', {'orders': orders})

