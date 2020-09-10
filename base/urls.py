from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name="home"),
    path('products/',views.product, name="product"),
    path('orders/',views.orders, name="orders"),
    path('list/',views.list, name="list"),
    path('categories/',views.category, name="category"),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base/home.html'), name='logout'),


]
