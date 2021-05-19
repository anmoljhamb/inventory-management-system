from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard_index, name="dashboard-index"),
    #Staff
    path('staff/', views.staff_index, name="staff-index"),
    path('staff_edit/<int:pk>', views.staff_edit, name="staff-edit"),
    path('staff_delete/<int:pk>', views.staff_delete, name="staff-delete"),
    #Product
    path('product/', views.product_index, name="product-index"),
    path('product_edit/<int:pk>', views.product_edit, name="product-edit"),
    path('product/delete/<int:pk>', views.product_delete, name="product-delete"),
    path('order/', views.order_index, name="order-index"),
    path('order_request/', views.order_request_index, name="order_request-index"),
    #Category
    path('category/', views.category_index, name="category-index"),
    path('category/edit/<int:pk>', views.category_edit, name="category-edit"),
    path('category/delete/<int:pk>', views.category_delete, name="category-delete"),
    #User paths
    path('register_user/', views.register_user, name="register-user"),
    path('user_login/', views.user_login, name="user-login"),
    path('logout/', views.user_logout, name="user-logout")
] 

