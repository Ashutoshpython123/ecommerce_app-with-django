from django.shortcuts import render, redirect, get_object_or_404
from . models import Item, OrderItem, Order, Address
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


# def Home(request):
#   context = {'item': Item.objects.all}
#  return render(request, 'index.html', context)

class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Item is successfully added into cart')
            return redirect("main:product", slug=slug)

        else:
            order.items.add(order_item)
            messages.info(request, 'Item is successfully added into cart')
            return redirect("main:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, 'Item is successfully added into cart')
        return redirect("main:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("main:product",slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("main:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("main:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("main:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:product", slug=slug)


def Order_Summary(request):
    return render(request, 'order_summary.html')


def checkout(request):
    return render(request, 'checkout.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New User Created: {username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'register.html')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request,
                          "register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request,
                  "register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("/")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username of password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})
