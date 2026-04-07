from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .models import Blog
from .models import Profile



def signup(request):
    
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')          # Collect email
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(username=name).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists',
                'show_login': True
            })

        # Create user with email
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        # Create user profile
        Profile.objects.create(
            user=user,
            mobile=mobile,
            address=address
        )

        return redirect('login')

    return render(request, 'signup.html')

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'items': items})


@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    if items.count() == 0:
        return redirect('home')

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
            payment_method=request.POST['payment']
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        items.delete()
        return render(request, 'success.html')

    return render(request, 'checkout.html')

@login_required
def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')
@login_required
def increase_qty(request, id):
    item = Cart.objects.get(id=id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_qty(request, id):
    item = Cart.objects.get(id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def blog_list(request):
    blogs= Blog.objects.all()
    return render(request, 'blog.html',{'blogs': blogs})

def blog_detail(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def profile(request):
    
    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        profile = Profile.objects.create(
            user=request.user,
            mobile="Not added",
            address="Not added"
        )

    return render(request, 'profile.html', {'profile': profile})

