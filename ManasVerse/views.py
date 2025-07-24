from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from decimal import Decimal
from .models import Product, Category, Order, OrderItem
from django.core.validators import RegexValidator
from django import forms
import logging

# For logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    sort_by = request.GET.get('sort')
    search_query = request.GET.get('q')

    if selected_category:
        products = products.filter(category__name=selected_category)
    if sort_by == 'low':
        products = products.order_by('price')
    elif sort_by == 'high':
        products = products.order_by('-price')
    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {'products': products, 'categories': categories}
    return render(request, 'products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_view')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart
    return redirect('cart_view')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_view')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def clear_session(request):
    request.session.flush()
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number')]
    )
    address = forms.CharField(widget=forms.Textarea)

def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', {})
            total_amount = Decimal('0.00')

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            order = Order.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                total_amount=0
            )

            for str_product_id, quantity in cart.items():
                try:
                    product_id = int(str_product_id)
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    total_price = product.price * quantity

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        total_price=total_price
                    )

                    total_amount += total_price

                except (Product.DoesNotExist, ValueError):
                    continue

            order.total_amount = total_amount
            order.save()

            # Clear cart
            request.session['cart'] = {}

            # Send Email
            try:
                subject = 'Your Order Confirmation'
                message = f'Thank you {name} for your order!\n\nOrder ID: {order.id}\nTotal: ₹{order.total_amount}\n\nWe will deliver it to:\n{address}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                logger.error(f"Email send failed: {e}")

            return redirect('order_summary', order_id=order.id)

        else:
            messages.error(request, "Please check the form for errors.")
            return render(request, 'checkout.html', {'form': form})

    form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})

def order_summary(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_summary.html', {'order': order})

def order_success(request):
    order = Order.objects.last()
    if not order:
        return redirect('home')

    items = order.orderitem_set.all()
    return render(request, 'order_success.html', {
        'order': order,
        'items': items,
        'total': order.total_amount,
    })

def dummy_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    request.session.flush()
    return redirect('payment_success', order_id=order.id)

def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'payment_success.html', {
        'order': order
    })
