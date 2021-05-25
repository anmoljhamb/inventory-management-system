from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from .models import GroupName, User, Category, Product, OrderRequest, Order
from .forms import CreateUserForm, GroupNameForm, CategoryForm, ProductForm, OrderRequestForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import csv, io


def execute_stuff(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        
        context = {
            'user': User.objects.get(id=request.user.id),
        }

        context['num_of_cat'] = context['user'].group_name.category_set.count()
        context['num_of_staff'] = context['user'].group_name.user_set.count()
        context['num_of_products'] = context['user'].group_name.product_set.count()
        context['num_of_order_request'] = context['user'].group_name.orderrequest_set.count()
        context['num_of_orders'] = context['user'].group_name.order_set.count()
        
        total_sale = 0
        for order in context['user'].group_name.order_set.all():
            total_sale += order.total_amount
        context['total_sale'] = total_sale

        return function(request, context, *args, **kwargs)
    return wrapper

def only_admin(function):
    @wraps(function)
    def wrapper(request, context, *args, **kwargs):

        if context['user'].user_type == "User":
            return HttpResponse("You are not authorized to access this content")

        return function(request, context, *args, **kwargs)
    return wrapper

'''
USER VIEWS BEGIN
'''
def register_user(request):

    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        shop_form = GroupNameForm(request.POST)


        if user_form.is_valid() and shop_form.is_valid():
            shop_instance = shop_form.save()
            instance = user_form.save(commit=False)
            instance.group_name = shop_instance
            instance.save()
            messages.success(request, "{} was successfully registered.".format(user_form.cleaned_data.get("username")))
            return redirect('user-login')
        else:
            user_form = CreateUserForm(request.POST)
            shop_form = GroupNameForm(request.POST)
    else:
        user_form = CreateUserForm()
        shop_form = GroupNameForm()

    user_form.fields['user_type'].choices = [("Group Admin", "Group Admin")]

    context = {
        'user_form': user_form,
        'shop_form': shop_form,
    }

    return render(request, "user/register_user.html", context)

def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.info(request, "Username or Password does not match any existing accounts.")

    context = {
        
    }

    return render(request, "user/user_login.html", context)

def user_logout(request):
    
    messages.info(request, f"{request.user.username} has been logged out.")
    logout(request)
    return redirect("user-login")

'''
USER VIEWS END
'''
def home(request):

    if request.user.is_authenticated:
        return redirect("dashboard-index")
    else:
        return redirect("user-login")

@login_required
@execute_stuff
def dashboard_index(request, context):

    orders = context['user'].group_name.order_set.all()
    products = {}
    for order in orders:
        if order.product.name in products:
            products[order.product.name] += order.total_amount
        else:
            products[order.product.name] = order.total_amount
            
    top_products = {k: v for k, v in sorted(products.items(), key=lambda item: item[1], reverse=True)}

    context['top_products'] = list(top_products.items())[:6]

    orders = context['user'].group_name.product_set.all()
    products = {}
    for order in orders:
        if order.name in products:
            products[order.name] += order.quantity
        else:
            products[order.name] = order.quantity
            
    top_products = {k: v for k, v in sorted(products.items(), key=lambda item: item[1], reverse=True)}

    context['top_stock'] = list(top_products.items())[:6]


    return render(request, "dashboard/dashboard_index.html", context)

@login_required
@execute_stuff
def category_index(request, context):

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.group_name = context['user'].group_name
            instance.save()
            messages.success(request, "The Category was successfully created.")
            return redirect('category-index')
    else:
        form = CategoryForm()

    user_categories = context['user'].group_name.category_set.all()

    context = {
        'user_categories': user_categories,
        'form': form,
        'button_value': "Create Category",
        'action_url': 'category_import',
        **context
    }

    return render(request, "dashboard/category_index.html", context)

@login_required
@execute_stuff
def category_import(request, context):
    if request.method == "POST":
        try:
            myfile = request.FILES.get("myfile")
            paramFile = io.TextIOWrapper(myfile)
            temp = csv.DictReader(paramFile)
            list_of_dict = list(temp)
            for row in list_of_dict:
                Category.objects.get_or_create(
                    name = row["name"],
                    group_name = context['user'].group_name
                )
            messages.info(request, "All the categories were imported successfully.")
        except Exception as E:
            print(E )
            messages.info(request, """
            The provided file is invalid. Make sure there is only 1 column, being "name", and all the 
            values must be included in double quotes.
            """)

    return redirect("category-index")

@login_required
@execute_stuff
@only_admin
def category_edit(request, context, pk):
    cat = Category.objects.get(id=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "Category was successfully changed.")
            return redirect("category-index")

    form = CategoryForm(instance=cat)

    context = {
        'form': form,
        'button_value': "Change",   
        **context
    }

    return render(request, "dashboard/category_edit.html", context)

@login_required
@execute_stuff
@only_admin
def category_delete(request, context, pk):
    cat = Category.objects.get(id=pk)

    if request.method == "POST":
        cat.delete()
        messages.success(request, "Category was deleted.")
        return redirect('category-index')

    return render(request, "dashboard/category_delete.html", context)


@login_required
@execute_stuff
def staff_index(request, context):

    context['curr_group_users'] = context['user'].group_name.user_set.all()
    context['button_value'] = "Create User"
    context['h3'] = 'Create an account for staff.'
    context['h4'] = '''A staff account will only be able to see the inventory, and make order requests
                    which will then be reviewed, edited and denied or approved by a shop admin. You can later, edit the user type too.'''
    

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.group_name = context['user'].group_name
            instance.save()
            messages.success(request, "The user was creaed successfully.")
            return redirect('staff-index')
    else:
        form = CreateUserForm()

    context['form'] = form
    return render(request, "dashboard/staff_index.html", context)


@login_required
@execute_stuff
@only_admin
def staff_edit(request, context, pk):

    temp_user = User.objects.get(id=pk)

    if request.method == "POST":
        form = CreateUserForm(request.POST, instance=temp_user)
        if form.is_valid():
            form.save()
            messages.success(request, "The user was changed successfully.")
            return redirect('staff-index')
    else:
        form = CreateUserForm(instance=temp_user)

    context['form'] = form
    context['button_value'] = "Change User"
    return render(request, "dashboard/staff_edit.html", context)


@login_required
@execute_stuff
@only_admin
def staff_delete(request, context, pk):
    item = User.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Staff was deleted.")
        return redirect('staff-index')

    return render(request, "dashboard/category_delete.html", context)

@login_required
@execute_stuff
def product_index(request, context):

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.group_name = context['user'].group_name
            instance.save()
            return redirect('product-index')
    else:
        form = ProductForm()
    
    context['form'] = form
    context['button_value'] = "Add Product"
    context['products'] = context['user'].group_name.product_set.all()
    context['action_url'] = "product_import"

    return render(request, "dashboard/product_index.html", context)

@login_required
@execute_stuff
@only_admin
def product_edit(request, context, pk):
    cat = Product.objects.get(id=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "product was successfully changed.")
            return redirect("product-index")

    form = ProductForm(instance=cat)

    context = {
        'form': form,
        'button_value': "Change",   
        **context
    }

    return render(request, "dashboard/product_edit.html", context)


@login_required
@execute_stuff
@only_admin
def product_delete(request, context, pk):
    cat = Product.objects.get(id=pk)

    if request.method == "POST":
        cat.delete()
        messages.success(request, "product was deleted.")
        return redirect('product-index')

    return render(request, "dashboard/category_delete.html", context)


@login_required
@execute_stuff
def product_import(request, context):
    if request.method == "POST":
        try:
            myfile = request.FILES.get("myfile")
            paramFile = io.TextIOWrapper(myfile)
            temp = csv.DictReader(paramFile)
            list_of_dict = list(temp)
            for row in list_of_dict:
                Product.objects.get_or_create(
                    name = row["Name"],
                    category = Category.objects.get_or_create(name=row["Category"], group_name=context['user'].group_name)[0],
                    quantity = row["Quantity"],
                    price_per_unit = row["Price Per Unit"],
                    group_name = context['user'].group_name
                )
            messages.info(request, "All the categories were imported successfully.")
        except Exception as E:
            print(E )
            messages.info(request, """
            The provided file is invalid. Make sure there are only 4 columns, being "Name", "Category", "Quantity", "Price Per Unit", and all the 
            values must be included in double quotes. Make sure the spelling of each is right, and that numbers shouldn't be in quotes and Category is one of the categories
            that have already been created, if it doesn't match, a new category will be created.
            """)

    return redirect("product-index")


@login_required
@execute_stuff
def order_index(request, context):

    context['orders'] = context['user'].group_name.order_set.all()
    context['action_url'] = "order_import"

    return render(request, "dashboard/order_index.html", context)

@login_required
@execute_stuff
def order_import(request, context):
    if request.method == "POST":
        try:
            myfile = request.FILES.get("myfile")
            paramFile = io.TextIOWrapper(myfile)
            temp = csv.DictReader(paramFile)
            list_of_dict = list(temp)
            for row in list_of_dict:
                temp_product = Product.objects.get(name=row["Name"])
                print(row)
                Order.objects.create(
                    product = temp_product,
                    staff = context['user'],
                    order_quantity = row["Quantity"],
                    group_name = context['user'].group_name,
                    total_amount = temp_product.price_per_unit*int(row["Quantity"])
                )
            messages.info(request, "All the categories were imported successfully.")
        except Exception as E:
            print(E)
            messages.info(request, """
            The provided file is invalid. Make sure there are only 2 columns, being "Product Name", "Order Quantity"and all the 
            values must be included in double quotes. Make sure the spelling of each is right, and that numbers shouldn't be in quotes and Product Name is one of the Products
            that have already been created.
            """)

    return redirect("order-index")


@login_required
@execute_stuff
@only_admin
def order_delete(request, context, pk):
    cat = Order.objects.get(id=pk)

    if request.method == "POST":
        cat.delete()
        messages.success(request, "Order was deleted.")
        return redirect('order-index')

    return render(request, "dashboard/category_delete.html", context)

@login_required
@execute_stuff
def order_request_index(request, context):

    if request.method == "POST":
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = context['user']
            instance.group_name = context['user'].group_name
            instance.total_amount = instance.order_quantity*instance.product.price_per_unit
            instance.save()
            return redirect('order_request-index')
    else:
        form = OrderRequestForm()

    if context['user'].user_type == "User":
        # form.fields['staff'].choices = [(context['user'], context['user'])]
        pass
    else:
        form.fields['staff'].queryset = context['user'].group_name.user_set.all()
    form.fields['product'].queryset = context['user'].group_name.product_set.all()
    form.fields['status'].choices = [("PENDING", "PENDING")]

    context['form'] = form
    context['button_value'] = "Add Order Request"
    context['order_requests'] = context['user'].group_name.orderrequest_set.all()

    return render(request, "dashboard/order_request_index.html", context)


@login_required
@execute_stuff
@only_admin
def order_request_edit(request, context, pk):
    cat = OrderRequest.objects.get(id=pk)

    if request.method == "POST":
        form = OrderRequestForm(request.POST, instance=cat)
        if form.is_valid():
            instance = form.save(commit=False)
            status = form.cleaned_data.get("status")

            if status == "APPROVED":
                if instance.product.quantity > instance.order_quantity:
                    Order.objects.create(
                        product = instance.product,
                        staff = instance.staff,
                        order_quantity = instance.order_quantity,
                        group_name = instance.group_name,
                        total_amount = instance.total_amount
                    )
                    pf = ProductForm(instance=instance.product)
                    pf = pf.save(commit=False)
                    pf.quantity -= instance.order_quantity
                    pf.save()
                    OrderRequest.objects.get(id=instance.id).delete()
                    messages.success(request, "Order Request was approved.")
                else:
                    messages.success(request, "Order Request couldn't be approved due to less stock.")
            elif status == "DENNIED":
                OderRequest.objects.get(instance=instance).delete()
                messages.success(request, "Order Request was denied.")
                
            return redirect("order_request-index")

    form = OrderRequestForm(instance=cat)

    context = {
        'form': form,
        'button_value': "Change",   
        **context
    }

    return render(request, "dashboard/order_request_edit.html", context)

@login_required
@execute_stuff
@only_admin
def order_request_delete(request, context, pk):
    cat = OrderRequest.objects.get(id=pk)

    if request.method == "POST":
        cat.delete()
        messages.success(request, "Order Request was deleted.")
        return redirect('order_request-index')

    return render(request, "dashboard/category_delete.html", context)