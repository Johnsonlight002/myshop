from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  get_object_or_404
from .models import Product, CartItem
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product

from django.contrib.auth.decorators import login_required
import stripe


stripe.api_key = "your_stripe_secret_key"

def home(request):
    products = Product.objects.all()
    
    # Retrieve cart from session (default to empty dict if not found)
    cart = request.session.get("cart", {})

    # Convert cart session data to a list of product details
    cart_items = []
    for product_id, quantity in cart.items():  # Quantity is an integer!
        try:
            product = Product.objects.get(id=int(product_id))
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image": product.image.url if product.image else None,
                "quantity": quantity  # No dictionary lookup!
            })
        except Product.DoesNotExist:
            continue  # Skip if product was deleted

    return render(request, "store/home.html", {
        "products": products,
        "cart_items": cart_items,
        "quantity_range": range(1, 11)  
    })

def checkout(request):
    return render(request, 'store/checkout.html')

def payment(request):
    return render(request, 'store/payment.html')

def login_view(request):
    return render(request, 'store/login.html')

def charge(request):
    if request.method == "POST":
        stripe.Charge.create(
            amount=5000,  # Amount in cents ($50.00)
            currency="usd",
            description="Payment for Order",
            source=request.POST['stripeToken']
        )
        return redirect('home')
   

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect after login
        else:
            print("Login failed. Errors:", form.errors)  # Debugging line
            messages.error(request, "Invalid username or password.")

    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can log in now.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        # Get existing cart from session or create an empty one
        cart = request.session.get("cart", {})

        # Update quantity if product exists, otherwise add it
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity

        # Save updated cart back to session
        request.session["cart"] = cart
        request.session.modified = True  # Mark session as modified

    return redirect("home")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("home")
