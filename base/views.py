from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Item, Order, ItemsOut
from .filters import ProductFilter, CategoryFilter
from .forms import ProductAddForm, CategoryAddForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.core import serializers


@login_required
def home(request):
    cat = Category.objects.filter(owner=request.user)
    prod = Product.objects.filter(owner=request.user)

    context = {
        'cat':cat,
        'prod':prod
    }
    return render(request, "base/home.html", context)



def chartData(request):
    try:
        data = Order.objects.values_list('year_month').annotate(price_sum=Sum("order_profit")).filter(user=request.user)
        order = Order.objects.filter(ordered=True)
        chartdata = []
        # a = ['a','b','c','d']
        # b = [10,20,30,40]


        for i in data:
            chartdata.append({i[0]:int(i[1])})

        # for i,j in zip(a,b):
        #     chartdata.append({i:j})

        return JsonResponse(chartdata, safe=False)
    except Exception:
        chartdata = []
        return JsonResponse(chartdata, safe=False)


@login_required
def product(request):
    try:
        products = Product.objects.filter(owner=request.user)
        noc = len(products)
        productfilter = ProductFilter(request.GET, queryset=products)
        products = productfilter.qs
    except Exception:
        products =""
        noc=""
        productfilter = ''
    
    context = {
        'noc':noc,
        'products':products,
        'productfilter':productfilter
    }
    return render(request, "base/products_page.html", context)


@login_required
def category(request):
    categories = Category.objects.filter(owner=request.user)
    noc = len(categories)
    print(noc)
    categoryfilter = CategoryFilter(request.GET, queryset=categories)
    categories = categoryfilter.qs
    context = {
        'noc':noc,
        'categories':categories,
        'categoryfilter':categoryfilter
    }
    return render(request, "base/category_page.html", context)


def signin(request):
    return render(request, 'converter/login.html')

@login_required
def orders(request):
    ordered_orders = Order.objects.filter(ordered=True, user=request.user).order_by('-ordered_date')
    context ={
        'ordered_orders':ordered_orders
    }
    print(ordered_orders)
    return render(request, 'base/orders.html', context)
    


@login_required
def list(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order':order
        }
        return render(request, 'base/list.html', context)
    except ObjectDoesNotExist:
        return redirect('home')

@login_required
def prodadd_request(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.save()
            form.save()
            messages.success(request, f'Product was added successfully!')
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ProductAddForm()
    return render(request, 'base/addproduct.html', {'form':form})


@login_required
def catadd_request(request):
    if request.method == 'POST':
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.save()
            form.save()
            messages.success(request, "Category was added successfully!")
            return HttpResponseRedirect(reverse('home'))
    else:
        form = CategoryAddForm()
    return render(request, 'base/addcategory.html', {'form':form})

    
 

def proddeleteconfirm(request, id):
    prod = get_object_or_404(Product, id=id)

    context = {
        'prod':prod
    }
    return render(request, 'base/productdelete_confirm.html', context)




def proddelete_request(request,id):
    Product.objects.get(id=id).delete()
    messages.info(request, "Product has been deleted!")
    return redirect('product')





def add_prod_quantity(request, id):
    prod = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        n = request.POST.get('add')
        
        prod.quantity = prod.add_quantity(n)
        prod.save()
        messages.success(request, "Product quantity was updated!")
        return redirect('product')
    
        



def sub_prod_quantity(request, id):
    prod = get_object_or_404(Product, id=id)
    
    n = request.POST.get('sub')

    try:
        a = int(n) + 0
        print("Number")

    except Exception:
        print("Not Numeric")
        n = 0

        messages.info(request, "Invalid Input!")
        return redirect('product')
    
    prod.quantity = prod.remove_quantity(n)
    prod.save()
    item = get_object_or_404(Product, id=id)
    order_item, created = Item.objects.get_or_create(
		user=request.user,
        ordered=False,
        item=item
		)
  
    try:
        if order_item.quantity == 0:
            if n.isnumeric():
                order_item.quantity = int(n)
                order_item.save()
    except Exception as e:
        print(e)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__id=item.id).exists():
            try:
                if n != "":
                    order_item.quantity += int(n)
                    order_item.save()
                    messages.info(request, "Item quantity updated!")
                    return redirect('product')
                else:
                    messages.error("Can't add an alphabet or Null as  a quantity!")

            except Exception:
                messages.error(request, "Try again!")
                return redirect()

        else:
            order.items.add(order_item)
            messages.info(request, "Item has been added to the Order List!")
            return redirect('product')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item has been added to the Order List!")
        return redirect('product')
   



# Editing and Updating  the Product and Category
def edit_product(request, id):
    prod = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductAddForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Updated!")
            return redirect('product')
    else:
        form = ProductAddForm(instance=prod)
    
    context = {
        'prod':prod,
        'form':form
    }
    return render(request, 'base/product_edit.html', context)


def edit_category(request, id):
    cat = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryAddForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated!")

            return redirect('category')
    else:
        form = CategoryAddForm(instance=cat)
    
    context = {
        'cat':cat,
        'form':form
    }
    return render(request, 'base/category_edit.html', context)



@login_required
def ordered(request, id):
    order = get_object_or_404(Order, id=id)
    order.ordered = True
    for item in order.items.all():
        item.ordered = True
        item.save()
    order.ordered_date = timezone.now()
    order.save()
    messages.success(request, "Your order has been saved!")
    return redirect('home')


def remove_from_order(request, id):
    item = Item.objects.get(id=id)
    item.item.quantity += item.quantity
    item.item.save()

    item.delete()
    messages.info(request, "Item has been removed!")
    return redirect('list')


def order_detail(request, id):
    order = Order.objects.get(id=id)
    context ={
        'order':order
    }
    return render(request, 'base/orderdetail.html', context)


def remove_from_ordered(request, id):
    Order.objects.get(id=id).delete()
    messages.info(request, "Order has been deleted!")
    return redirect('orders')



def orderdeleteconfirm(request, id):
    order = get_object_or_404(Order, id=id)

    context = {
        'order':order
    }

    return render(request, 'base/confirm_ordered_delete.html', context)


def catdelete(request, id):
    Category.objects.get(id=id).delete()
    return redirect('category')
    

def cat_delete_confirm(request, id):
    cat = get_object_or_404(Category, id=id)


    context = {
        'cat':cat
    }
    return render(request, 'base/cat_delete_confirm.html', context)