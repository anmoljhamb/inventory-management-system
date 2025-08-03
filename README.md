# Inventory Management System

The Inventory Management System consists of two types of users: an **abstract user** and a **group admin**.

* Each **group admin** is a shop owner who can create an account for their shop and add users from their dashboard.
* Each **user** can make an order request, which can only be approved by a group admin.
* The dashboard includes pages for **Orders**, **Order Requests**, **Products**, **Categories**, **Staff**, and a **Home page**.

---

## Admin Login

The default superuser credentials for `/admin` are:

* **Username**: `admin`
* **Password**: `admin`

You can also create your own superuser with:

```bash
python manage.py createsuperuser
```

---

## Pages

1. **Home Page**
   ![Home Page Screenshot](screenshots/ss_1.png)
   Displays basic shop information and statistical charts.

2. **Staff Page**
   Displays all information about the users and group admins of a particular shop.

3. **Order and Order Requests Pages**
   Allows group admins to delete or view orders.
   On the **Order Requests** page, group admins can approve or deny user order requests.

4. **Product and Category Pages**

   * Users can only view products and categories.
   * Group admins can perform full CRUD operations.

---

## Models

1. **GroupName**

   * The key model that links all others together.
   * Contains a single `CharField`.
   * Acts as a foreign key for other models, enabling multi-shop support.

2. **User**

   * Extends `django.contrib.auth.models.User`.
   * Contains additional fields to eliminate the need for a separate Profile model.

3. **Category**

   * Contains:

     * `name`: `CharField`
     * `group_name`: `ForeignKey` to `GroupName`, differentiating categories per shop.

4. **Product**

   * Stores all product-related information.
   * Linked to a `GroupName` for multi-shop support.

5. **OrderRequest** and **Order**

   * Identical models except for the `status` field.
   * When an `OrderRequest` is approved, it's converted to an `Order` and the original request is deleted.

---

## Running the Application

1. **Clone or download** the project:

   ```bash
   git clone <repository_url>
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

---

## TODO

1. Review and improve website security.
2. Add more statistical charts and insights.

---
