from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_index, name="dashboard-index"),
    path('staff/', views.staff_index, name="staff-index"),
    path('product/', views.product_index, name="product-index"),
    path('order/', views.order_index, name="order-index"),
    path('order_request/', views.order_request_index, name="order_request-index"),
    path('category/', views.category_index, name="category-index"),
] 

