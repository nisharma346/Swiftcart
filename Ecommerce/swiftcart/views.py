from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, CustomUserRegistrationForm
from .models import Category, CustomUser, GalleryImage, Product, Contact,Announcement
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from django.http import JsonResponse

# Create your views here.
def home(request):
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)

    context = {
        "featured_products": featured_products,
        "categories": categories,
    }

    return render(request, "swiftcart/home.html", context)


@require_http_methods(["GET", "POST"])
def register(request):
    """
    User registration view
    GET: Display the registration form
    POST: Process the registration form
    """
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Registration successful! Please log in with your email and password.'
            )
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register'
    }
    return render(request, 'swiftcart/register.html', context)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    User login view
    GET: Display the login form
    POST: Process the login form
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Get user by email
            user = CustomUser.objects.get(email=email)
            # Authenticate with username (since username is set to email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                # Redirect to next page or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    context = {
        'page_title': 'Login'
    }
    return render(request, 'swiftcart/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def product_list(request):
    products = Product.objects.filter(is_active=True)

    context = {
        "products": products,
        "page_title": "Products",
        "page_heading": "Our Products",
        "page_subtitle": "Browse available items and view product details.",
    }

    return render(request, "swiftcart/product_list.html", context)


def product_detail(request, slug):
    product = Product.objects.filter(
        slug=slug,
        is_active=True
    ).first()

    if not product:
        return render(
            request,
            "swiftcart/404.html",
            {"page_title": "Product Not Found"},
            status=404
        )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
    "product": product,
    "related_products": related_products,
    "page_title": product.name,
    "page_heading": product.name,
}

    return render(request, "swiftcart/product_detail.html", context)

def category_list(request):
    """Display all active categories."""
    categories = Category.objects.filter(is_active=True)[:6]

    context = {
        'categories': categories,
        'page_title': 'Categories'
    }
    return render(request, 'swiftcart/category.html', context)


def category_detail(request, slug):
    """Display a single category and its active products."""
    category = Category.objects.filter(slug=slug, is_active=True).first()
    if not category:
        return render(request, 'swiftcart/404.html', {'page_title': 'Category not found'}, status=404)

    products = category.products.filter(is_active=True).order_by('created_at')
    context = {
        'category': category,
        'products': products,
        'page_title': category.name
    }
    return render(request, 'swiftcart/category_detail.html', context)


def gallery(request):
    """Display all active gallery images."""
    images = GalleryImage.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'images': images,
        'page_title': 'Gallery'
    }
    return render(request, 'swiftcart/gallery.html', context)


def about_us(request):
    context = {
        "page_title": "About Us",
        "page_heading": "About Us",
        "page_subtitle": "Learn more about SwiftCart and our commitment to quality, trust, and customer satisfaction.",
    }
    return render(request, "swiftcart/about.html", context)


@require_http_methods(["GET", "POST"])
def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            # Save or process form here if needed
            messages.success(
                request,
                "Thank you! Your message has been sent successfully."
            )
            return redirect("contact")

    else:
        form = ContactForm()

    context = {
        "form": form,
        "page_title": "Contact Us",
        "page_heading": "Contact Us",
        "page_subtitle": "Have a question or need assistance? We'd love to hear from you.",
    }

    return render(request, "swiftcart/contact.html", context)
def cart(request):

    cart = request.session.get("cart", {})

    cart_items = []

    grand_total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(
    Product,
    slug=slug,
    is_active=True
)
        if product:

            total = product.price * quantity

            grand_total += total

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "total": total,
            })

    context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
        "page_title": "Shopping Cart",
        "page_heading": "Shopping Cart",
        "page_subtitle": "Review your selected products before checkout."
    }

    return render(request, "swiftcart/cart.html", context)
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")
def wishlist(request):

    wishlist = request.session.get("wishlist", {})

    wishlist_items = []

    for product_id in wishlist.keys():
        product = Product.objects.filter(id=product_id).first()
        if product:
            wishlist_items.append(product)

    context ={
       "products": wishlist_items,
        "wishlist": wishlist,
        "wishlist_items": wishlist_items,
        "page_title": "Wishlist",
        "page_heading": "My Wishlist",
        "page_subtitle": "Save your favourite products for later.",
    }

    return render(request, "swiftcart/wishlist.html", context)

def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    wishlist = request.session.get("wishlist", {})

    wishlist[str(product_id)] = True

    request.session["wishlist"] = wishlist

    messages.success(request, f"{product.name} added to wishlist.")

    return redirect("wishlist")


def remove_from_wishlist(request, product_id):

    wishlist = request.session.get("wishlist", {})

    product_id = str(product_id)

    if product_id in wishlist:
        del wishlist[product_id]

    request.session["wishlist"] = wishlist

    return redirect("wishlist")
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def checkout(request):

    cart = request.session.get("cart", {})

    cart_items = []

    grand_total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.filter(id=product_id).first()

        if product:

            total = product.price * quantity

            grand_total += total

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "total": total,
            })

    context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
        "page_title": "Checkout",
        "page_heading": "Checkout",
        "page_subtitle": "Complete your order securely.",
    }

    return render(request, "swiftcart/checkout.html", context)
@login_required(login_url="login")
def place_order(request):

    if request.method == "POST":

        cart = request.session.get("cart", {})

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        grand_total = 0

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST["full_name"],
            email=request.POST["email"],
            mobile=request.POST["mobile"],
            address=request.POST["address"],
            city=request.POST["city"],
            state=request.POST["state"],
            pincode=request.POST["pincode"],
            total_amount=0
        )

        for product_id, quantity in cart.items():

            product = Product.objects.get(id=product_id)

            total = product.price * quantity

            grand_total += total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        order.total_amount = grand_total
        order.save()

        request.session["cart"] = {}

        messages.success(request, "Order placed successfully!")

        return redirect("order_success")

    return redirect("checkout")
@login_required(login_url="login")
def order_success(request):

    context = {
        "page_title": "Order Success",
        "page_heading": "Order Placed Successfully",
        "page_subtitle": "Thank you for shopping with SwiftCart."
    }

    return render(request, "swiftcart/order_success.html", context)
def toggle_wishlist(request, product_id):

    wishlist = request.session.get("wishlist", {})

    product_id = str(product_id)

    if product_id in wishlist:
        del wishlist[product_id]
        status = "removed"
    else:
        wishlist[product_id] = True
        status = "added"

    request.session["wishlist"] = wishlist

    return JsonResponse({
        "status": status,
        "count": len(wishlist)
    })
def ajax_add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session["cart"] = cart

    return JsonResponse({
        "count": sum(cart.values())
    })
# ================= STATIC PAGES =================

def privacy(request):
    return render(request, 'swiftcart/privacy.html', {
        'page_heading': 'Privacy Policy',
        'page_title': 'Privacy Policy',
    })


def refund(request):
    return render(request, 'swiftcart/refund.html', {
        'page_heading': 'Refund Policy',
        'page_title': 'Refund Policy',
    })


def shipping(request):
    return render(request, 'swiftcart/shipping.html', {
        'page_heading': 'Shipping Policy',
        'page_title': 'Shipping Policy',
    })


def terms(request):
    return render(request, 'swiftcart/terms.html', {
        'page_heading': 'Terms & Conditions',
        'page_title': 'Terms & Conditions',
    })


def mission(request):
    return render(request, 'swiftcart/mission.html', {
        'page_heading': 'Our Mission',
        'page_title': 'Our Mission',
    })


def vision(request):
    return render(request, 'swiftcart/vision.html', {
        'page_heading': 'Our Vision',
        'page_title': 'Our Vision',
    })
@login_required(login_url="login")
def profile(request):

    context = {

        "page_title": "My Profile",

        "page_heading": "My Profile",

        "page_subtitle": "Manage your personal information.",

    }

    return render(
        request,
        "swiftcart/profile.html",
        context
    )
@login_required(login_url="login")
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.full_name = request.POST.get("full_name")
        user.email = request.POST.get("email")
        user.mobile_no = request.POST.get("mobile_no")
        user.alternate_mobile_no = request.POST.get("alternate_mobile_no")
        user.dob = request.POST.get("dob")
        user.gender = request.POST.get("gender")
        user.address = request.POST.get("address")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    context = {

        "page_title": "Edit Profile",

        "page_heading": "Edit Profile",

        "page_subtitle": "Update your personal information.",

    }

    return render(request, "swiftcart/edit_profile.html", context)