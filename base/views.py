from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .filters import ProductFilter, CategoryFilter


@login_required
def home(request):
    return render(request, "base/home.html")


def product(request):
    products = Product.objects.all()
    productfilter = ProductFilter(request.GET, queryset=products)
    products = productfilter.qs
    context = {
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
