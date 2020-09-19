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
    path('add-product/',views.prodadd_request, name="addprod"),
    path('add-category/',views.catadd_request, name="addcat"),
    path('products/deleted/<int:id>/', views.proddelete_request, name="proddelete"),
    path('products/delete-confirm/<int:id>/', views.proddeleteconfirm, name="prodconfirm"),
    path('products/addquantity/<int:id>/', views.add_prod_quantity, name="addquan"),
    path('products/removequantity/<int:id>/', views.sub_prod_quantity, name="subquan"),
    path('products/edit/<int:id>/', views.edit_product, name="editproduct"),
    path('categories/edit/<int:id>/', views.edit_category, name="editcategory"),
    path('saved/<int:id>/', views.ordered, name="save_order"),
    path("list/remove/<int:id>/", views.remove_from_order, name="remove_from_order"),
    path("ordered/<int:id>/", views.order_detail, name="orderdetail"),
    path("ordered/remove/<int:id>/", views.remove_from_ordered, name="remove_ordered"),
    path('ordered/delete-confirm/<int:id>/', views.orderdeleteconfirm, name="orderconfirm"),
    path('categories/delete-confirm/<int:id>/', views.cat_delete_confirm, name="delete_confirm"),
    path("categories/delete/<int:id>/", views.catdelete, name="delete_cat"),


]