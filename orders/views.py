from django.shortcuts import render, redirect
from .models import Cart, CartItem
from books.models import Books
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='/users/login/')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_items = CartItem.objects.filter(cart = cart)
    total_amount = sum(cart_item.total_price for cart_item in cart_items)
    


    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})



@login_required(login_url='/users/login')
def add_cart_item(request, pk):

    books = Books.objects.get(pk = pk)

    cart, created = Cart.objects.get_or_create(user = request.user)
    if books.stock > 0:
        cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product = books)

        if not cart_item_created:
            cart_item.quantity += 1
        elif cart_item_created:
            cart_item.quantity = 1
        cart_item.save()


    return redirect(request.META.get('HTTP_REFERER'))

class AddCartItem(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        books = Books.objects.get(pk = pk)
        cart, created = Cart.objects.get_or_create(user = request.user)

        if books.stock > 0:
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product = books)

            if not cart_item_created:
                cart_item.quantity += 1
            elif cart_item_created:
                cart_item.quantity = 1
            cart_item.save()

        return redirect(request.META.get('HTTP_REFERER'))           



@login_required(login_url='/users/login')
def update_cart_item(request, pk):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(pk=pk)
        up_quantity = int(request.POST.get('quantity'))
        if up_quantity == 0:
            cart_item.delete()
        elif up_quantity <= cart_item.product.stock:
            cart_item.quantity = up_quantity
            cart_item.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

class UpdateCartItemView(View):
    @staticmethod
    def post(request, pk):
        cart_item = CartItem.objects.get(pk=pk)
        up_quantity = int(request.POST.get('quantity'))
        if up_quantity == 0:
            cart_item.delete()
        elif up_quantity <= cart_item.product.stock:
            cart_item.quantity = up_quantity
            cart_item.save()
        
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/login')
def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

