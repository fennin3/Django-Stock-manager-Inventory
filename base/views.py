from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .filters import ProductFilter, CategoryFilter
from .forms import ProductAddForm, CategoryAddForm


@login_required
def home(request):
    return render(request, "base/home.html")


def product(request):
    products = Product.objects.all()
    noc = len(products)
    productfilter = ProductFilter(request.GET, queryset=products)
    products = productfilter.qs
    context = {
        'noc':noc,
        'products':products,
        'productfilter':productfilter
    }
    return render(request, "base/products_page.html", context)

def category(request):
    categories = Category.objects.all()
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


def orders(request):
    return render(request, 'base/orders.html')


def list(request):
    return render(request, 'base/list.html')


def prodadd_request(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.save()
            form.save()
            messages.success(request, f'Your request was posted!')
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ProductAddForm()
    return render(request, 'base/addproduct.html', {'form':form})



def catadd_request(request):
    if request.method == 'POST':
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.owner = request.user
            fm.save()
            form.save()
            messages.success(request, f'Your request was posted!')
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
    
    return redirect('product')

def add_prod_quantity(request, id):
    prod = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        n = request.POST.get('add')
        
        prod.quantity = prod.add_quantity(n)
        prod.save()

        return redirect('product')

def sub_prod_quantity(request, id):
    prod = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        n = request.POST.get('sub')
        
        prod.quantity = prod.remove_quantity(n)
        prod.save()

        return redirect('product')
    
def edit_product(request, id):
    prod = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductAddForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductAddForm(instance=prod)
    
    context = {
        'prod':prod,
        'form':form
    }
    return render(request, 'base/product_edit.html', context)


