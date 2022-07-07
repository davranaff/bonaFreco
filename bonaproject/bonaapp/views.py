from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.core.mail import send_mail


# Create your views here.


def home_page(request):
    search = request.GET.get('search')
    product = Product.objects.all()

    paginator = Paginator(
        product,
        12,
        orphans=0,
        allow_empty_first_page=False,
    )
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    result = None
    products = None
    if search:
        products = product.filter(Q(name__icontains=search))
        if product: result = True
    slider = Slider.objects.all()
    return render(request, 'home_page.html', {
        'product': product,
        'products': products,
        'slider': slider,
        'result': result,
        'search': search,
        'page': page,
        'paginator': paginator
    })


def subcategory_detail(request, pk):
    categories = SubCategory.objects.get(pk=pk)
    return render(request, 'category-detail.html', {'subcategory': categories})


# cart create

def add_to_cart(request, pk):
    kol = float(request.GET.get('kol'))
    if kol > 0:
        product = Product.objects.get(pk=pk)
        basket = Basket.objects.filter(owner=request.user, product=product)
        for item in basket:
            if item.product == product:
                item.quantity = kol
                item.save()
                return redirect('bonaapp:cart_url')
        Basket.objects.create(owner=request.user, product=product, quantity=kol)
        return redirect('bonaapp:cart_url')
    else:
        messages.error(request, 'You can\'t add to cart because the quantity must be greater than zero')
        return redirect('bonaapp:cart_url')


# delete cart item

def delete_cart_item(request):
    basket_pk = request.GET.get('basket_pk')
    buylater_pk = request.GET.get('buylater_pk')
    if buylater_pk:
        buylater = BuyLater.objects.get(pk=buylater_pk)
        buylater.delete()
        return redirect('bonaapp:cart_url')
    if basket_pk:
        basket = Basket.objects.get(pk=basket_pk)
        basket.delete()
        return redirect('bonaapp:cart_url')


def cart(request):
    date_now = datetime.date.today()
    cart_list = Basket.objects.filter(owner=request.user)
    quantity = None
    for item in cart_list:
        if item.quantity > 0:
            quantity = 1
    cart_later = BuyLater.objects.filter(owner=request.user)
    return render(request, 'cart.html',
                  {'cart': cart_list, 'date_now': date_now, 'cart_later': cart_later, 'quantity': quantity})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    products = Product.objects.all()[:12]
    return render(request, 'product_detail.html', {
        'product': product,
        'products': products
    })


def create_order(request):
    order = Order.objects.filter(owner=request.user).order_by('-date')
    basket = Basket.objects.filter(owner=request.user)
    amount = sum([item.quantity for item in basket])
    total = sum([item.total_price() for item in basket])
    form = CrateOrder(request.POST)
    address = request.POST.get('address')
    telephone_number = request.POST.get('telephone_number')
    for empty in basket:
        if empty.quantity:
            if address and telephone_number:
                order = Order.objects.create(
                    address=address,
                    email=request.user.email,
                    telephone_number=telephone_number,
                    owner=request.user,
                    buy=True,
                    date=datetime.datetime.now()
                )
                if order.buy:
                    product_list = []
                    for item in basket:
                        OrderProduct.objects.create(
                            order=order,
                            product=item.product,
                            amount=amount,
                            total=total,
                        )
                        my_dict = {
                            'name': item.product.name,
                            'amount': item.quantity,
                            'total': item.total_price(),
                            'is_drink': item.product.is_drink
                        }
                        product_list.append(my_dict)
                    send_to_mail(
                        address=order.address,
                        telephone=order.telephone_number,
                        date=order.date,
                        product_list=product_list,
                        user=request.user.username,
                        email=request.user.email
                    )
                    basket.delete()
                    messages.success(request, 'Your item has been successfully processed')
                    return redirect('bonaapp:history_order_url')
        else:
            messages.error(request, 'You can\'t add to cart because the quantity must be greater than zero')
            return redirect('bonaapp:cart_url')
    return render(request, 'order.html', {
        'basket': basket,
        'amount': amount,
        'total': total,
        'order': order,
        'form': form
    })


def send_to_mail(address, telephone, date, product_list, user, email):
    template = []
    total_price = 0
    for item in product_list:
        x = f"name: {item['name']}, amount: {item['amount']}, total: {item['total']} AED"
        total_price += item['total']
        template.append(x)
    send_mail(
        f'BonaFresco',
        f'Client name: {user}\n\n'
        f'products \n\n{template}\n\n'
        f'total price: {total_price} AED \n\n'
        f'telephone: {telephone}\n\n'
        f'date: {date}\n\n'
        f'address: {address}\n\n'
        f'email: {email}',
        'bonafresco@gmail.com',
        recipient_list=[email, 'bonafresco@gmail.com']
    )


def history_order(request):
    order = Order.objects.filter(owner=request.user).order_by('-date')
    return render(request, 'history_order.html', {'order': order})


def buylater(request, pk):
    date = request.GET.get('date')
    if date:
        basket = Basket.objects.get(pk=pk)
        BuyLater.objects.create(
            owner=request.user,
            date=date,
            product=basket.product,
            quantity=basket.quantity,

        )
        basket.delete()
        messages.success(request, 'The product was successfully added to the "buy later" list')
        return redirect('bonaapp:cart_url')


def buynow(request, pk):
    now = BuyLater.objects.get(pk=pk)
    Basket.objects.create(
        owner=request.user,
        product=now.product,
        quantity=now.quantity,
    )
    now.delete()
    return redirect('bonaapp:cart_url')


def return_order(request, pk):
    order = Order.objects.get(pk=pk)
    for item in order.order_product.all():
        Basket.objects.create(
            owner=request.user,
            product=item.product,
            quantity=0
        )
    return redirect('bonaapp:cart_url')


def about(request):
    return render(request, 'about.html')
