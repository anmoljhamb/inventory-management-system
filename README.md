# inventory-management-system

Inventory Management System. 
The System consist of two types of users, an abstract user, and a group admin. Now, every group admin, is a shop owner, which can make an account for his or her own shop, and he can add users from the dashboard. Each user can make an order request, which can only be approved by a group admin. The dashboard contains different pages, including Order, Order Requests, Product, Category, Staff, and home page. 

# Admin login
The default superuser login for /admin is, 
username: admin
password: admin
You can add your own superuser by the command, python manage.py createsuperuser

# Pages
<ol>
<li>
    Home Page
    <img src="screenshots/ss_1.png">
    This Page contains the basic information, the statics charts.
</li>
<li>
    Staff Page
    This page contains all the information of the users and group admins of that particular shop.
</li>
<li>
    Order and Order Requests Page
    These pages would allow the group admin to delete and view the orders, and in case of order requests, deny or approve a request.
</li>
<li>
    Product and Category Page
    This Page contains all the information about the products and categories. A user can just view them, whereas, the group admin can do CRUD operations
</li>
</ol>

# Models used in the application.

<ol>
<li>
    <b>Group Name</b>
    This is the most important model out of all. This allows the app to separate the users, products, and all other models. This contains just a single CharField. This Model acts as a foreign key to the rest of the models, which allows us to establish many to one relationship, giving us easier access of the particular objects.
</li>
<li>
    <b>User</b>
    As the name states, this model is the user model, which allows the user to login into the application. This model overrides the django.contrib.auth.models.User in order to get more fields into a single model, in order to not have to create a separate Profile model
</li>
<li>
    <b>Category</b>
    Category Model contains a single CharField, "name", and a ForeignKey group_name, which allows us to differentiate categories created by separate shops.
</li>
<li>
    <b>Product</b>
    Product Model contains all the information about a product and a ForeignKey group_name, which allows us to differentiate products created by separate shops.
</li>
<li>
    <b>Orderrequest and Order</b>
    The only difference between OrderRequest model and the Order Model is the CharField status. When a OrderRequest's status is changed to approved, the rest of the model is created as Order, and the original one is deleted.
</li>
</ol>

# Steps to run the website.
<ul>
Download the zip, and extract it to a folder. You can use the git clone command too.
</ul>
<ul>
Install the requirements by running the command:
pip install -r requirements.txt
</ul>
<ul>
Run the server by the command
python manage.py runserver
</ul>

# Todo
<ol>
<li>
    Checkout if the website's security is good enough.
</li>
<li>
    Add more charts with different stats.
</li>
</ol>

If you have any suggestions, feel free to drop an email at codingwithaj@gmail.com, or DM on instagram on @thetechgeek_