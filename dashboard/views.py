from django.shortcuts import render
from django.http import HttpResponse
from functools import wraps


def execute_stuff(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        print("Executing before the function")
        return function(request, *args, **kwargs)
    return wrapper

@execute_stuff
def dashboard_index(request):
    return render(request, "dashboard/dashboard_index.html")

@execute_stuff
def category_index(request):
    return render(request, "dashboard/category_index.html")

def staff_index(request):
    return render(request, "dashboard/staff_index.html")

def product_index(request):
    return render(request, "dashboard/product_index.html")

def order_index(request):
    return render(request, "dashboard/order_index.html")

def order_request_index(request):
    return render(request, "dashboard/order_request_index.html")
