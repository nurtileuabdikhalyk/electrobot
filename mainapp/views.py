from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from .models import Category, Product, Order, Customer
from .forms import ContactForm, OrderForm, LoginForm, SignUpForm


def index(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    if request.method == 'POST':
        p = request.POST.get('p')
        remove = request.POST.get('remove')

        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(p)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(p)
                    else:
                        cart[p] = quantity - 1
                else:
                    cart[p] = quantity + 1

            else:
                cart[p] = 1
        else:
            cart = {}
            cart[p] = 1

        request.session['cart'] = cart
    categories = Category.objects.all()
    products = Product.objects.order_by('-created')[:8]
    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()

    context = {
        'title': 'ElectroBot',
        'products': products,
        'categories': categories,
        'total_quantity': total_quantity,
        'order_count': order_count
    }
    return render(request, 'mainapp/index.html', context)


# admin
# asem


def contact(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('home')
    form = ContactForm()

    context = {
        'title': 'Контакт',
        'form': form,
        'total_quantity': total_quantity,
    }
    return render(request, 'mainapp/contact.html', context)


def category(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    categories = Category.objects.all()
    products = Product.objects.order_by('-created')

    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()
    context = {
        'title': 'Барлық тауарлар',
        'products': products,
        'categories': categories,
        'total_quantity': total_quantity,
        'order_count': order_count
    }
    return render(request, 'mainapp/categories.html', context)


def categories(request, slug):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()
    context = {
        'title': category.name,
        'products': products,
        'categories': categories,
        'total_quantity': total_quantity,
        'order_count': order_count
    }
    return render(request, 'mainapp/categories.html', context)


def product(request, slug):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    products = Product.objects.filter(category=product.category).order_by('-created')[:4]
    if request.method == 'POST':
        p = request.POST.get('p')
        remove = request.POST.get('remove')

        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(p)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(p)
                    else:
                        cart[p] = quantity - 1
                else:
                    cart[p] = quantity + 1

            else:
                cart[p] = 1
        else:
            cart = {}
            cart[p] = 1

        request.session['cart'] = cart
        return redirect(reverse('product', kwargs={"slug": product.slug}))
    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()
    context = {
        'title': product.name,
        'categories': categories,
        'product': product,
        'products': products,
        'total_quantity': total_quantity,
        'order_count': order_count
    }
    return render(request, 'mainapp/product.html', context)


@login_required
def order(request):
    categories = Category.objects.all()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    customer = request.session.get('customer')
    orders = Order.objects.filter(customer=customer).order_by('status', '-date')
    context = {
        'title': 'Тапсырыс',
        'orders': orders,
        'total_quantity': total_quantity,
        'categories': categories,

    }
    return render(request, 'mainapp/order.html', context)


def cart(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())

    categories = Category.objects.all()

    ids = list(request.session.get('cart').keys())

    products = Product.objects.filter(id__in=ids)
    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()
    context = {
        'title': 'Себет',
        'categories': categories,
        'products': products,
        'total_quantity': total_quantity,
        'order_count': order_count
    }
    return render(request, 'mainapp/cart.html', context)


@login_required
def checkout(request):
    categories = Category.objects.all()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        total_quantity = 0
    else:
        total_quantity = sum(cart.values())
    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in=ids)
    customer = request.session.get('customer')
    order_count = Order.objects.filter(customer=customer).filter(status=True).count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            city = request.POST.get('city')
            street = request.POST.get('street')
            house = request.POST.get('house')
            house_number = request.POST.get('house_number')
            customer = request.session.get('customer')
            oplata = request.POST.get('oplata')
            for product in products:
                p = product.price
                if order_count >= 3:
                    p = product.price * 90 / 100
                Order.objects.create(customer=Customer.objects.get(id=customer),
                                     product=product,
                                     price=p,
                                     quantity=cart.get(str(product.id)),
                                     city=city,
                                     street=street,
                                     house=house,
                                     house_number=house_number,
                                     oplata=oplata,
                                     )
            request.session['cart'] = {}
            return redirect('home')
    form = OrderForm()

    context = {
        'title': 'Тапсырыс беру',
        'categories': categories,
        'products': products,
        'total_quantity': total_quantity,
        'form': form,
        'order_count': order_count
    }
    return render(request, 'mainapp/checkout.html', context)


class Search(ListView):
    categories = Category.objects.all()
    template_name = 'mainapp/search.html'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Іздеу'
        context['categories'] = categories
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def signin(request):
    messages = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            request.session['customer'] = Customer.objects.get(user=user).id
            # print(request.session['customer'] )
            try:
                auth.login(request, user)
            except:
                context = {'title': 'Кіру', 'form': form, 'messages': 'Логин немесе пароль қате!'}
                return render(request, 'mainapp/signin.html', context)
            return redirect('home')
    else:
        form = LoginForm()
    context = {'title': 'Кіру', 'form': form, 'messages': messages}
    return render(request, 'mainapp/signin.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            Customer.objects.create(user=user,
                                    first_name=form.cleaned_data['first_name'],
                                    last_name=form.cleaned_data['last_name'],
                                    phone=form.cleaned_data['phone'],

                                    )
            request.session['customer'] = Customer.objects.get(user=user).id
            return redirect('home')

    else:
        form = SignUpForm()
    context = {'title': 'Тіркелу', 'form': form}
    return render(request, 'mainapp/sign-up.html', context)


def logout(request):
    auth.logout(request)
    request.session.clear()
    return redirect('account_signin')
