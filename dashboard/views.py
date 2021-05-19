from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from .models import GroupName, User, Category
from .forms import CreateUserForm, GroupNameForm, CategoryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def execute_stuff(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        
        context = {
            'user': User.objects.get(id=request.user.id),
        }

        context['num_of_cat'] = context['user'].group_name.category_set.count()
        context['num_of_staff'] = context['user'].group_name.user_set.count()

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
        **context
    }

    return render(request, "dashboard/category_index.html", context)

@login_required
@execute_stuff
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
    return render(request, "dashboard/product_index.html", context)

@login_required
@execute_stuff
def order_index(request, context):
    return render(request, "dashboard/order_index.html", context)

@login_required
@execute_stuff
def order_request_index(request, context):
    return render(request, "dashboard/order_request_index.html", context)
