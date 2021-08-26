from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from kitchen.models import Item, Kitchen
from .cart import Cart
from .forms import CartAddProductForm
# from coupons.forms import CouponApplyForm



@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    # form = CartAddProductForm(request.POST)
    path = '/kitchen/' + str(item.kitchen_id)

    cart.add(item=item,
             quantity=1,
             update_quantity=False
             )

    return redirect(path)


@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    path = '/cart'
    return redirect(path)


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    kitchen_name = {}
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    # coupon_apply_form = CouponApplyForm()

    cart_items = [i['item'] for i in cart]

    kitchen = ''
    for i in cart_items:
        kitchen = Kitchen.objects.all()
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'kitchen': kitchen,
                                                # 'coupon_apply_form': coupon_apply_form
                                                })
