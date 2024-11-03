# LittleLemonAPI

## Overview

The **Little Lemon API** is a Django-based backend project designed to handle an order management system with distinct roles and permissions for customers, managers, and delivery crew members. The API supports operations for managing menu items, user-specific cart items, and processing orders with robust permission handling.

## Table of Contents
- [Features](#features)
- [Roles and Permissions](#roles-and-permissions)
- [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Sample Requests](#sample-requests)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Role Management**: Three distinct roles (Manager, Customer, Delivery Crew) with specific access control.
- **Menu Management**: Allows managers to add, update, delete, and view menu items.
- **Cart Management**: Enables customers to add items to a cart and proceed with an order.
- **Order Processing**: Manages order creation, status updates, and order assignment to the delivery crew.
- **Pagination & Filtering**: Supports pagination and status filtering for orders.
- **Role-Based Access Control (RBAC)**: Enforces role-based access with granular permissions for all actions.

## Roles and Permissions

1. **Manager**: 
   - Manage menu items (create, update, delete).
   - View all orders and update delivery crew assignments and statuses.
   - Delete orders.
  
2. **Customer**: 
   - Add items to the cart, view cart, and place orders.
   - View only their own orders.

3. **Delivery Crew**: 
   - View orders assigned to them.
   - Update order status to reflect delivery progress.
  
## Installation

### Prerequisites
- Python 3.x
- Django 5.x
- Django REST Framework

### Setup

1. **Clone the repository**:

```bash
git clone https://github.com/AflaxCade/LittleLemonAPI.git
```

2. **Navigate to the project directory**:
 
```bash
cd LittleLemonAPI
```

3. **Create a virtual environment**:

```bash
python -m venv env
```

4. **Activate the virtual environmen**t:

- For Windows:

```bash
env\Scripts\activate
```

- For macOS and Linux:

```bash
source env/bin/activate
```

5. **Install the required dependencies**:

```bash
pip install -r requirements.txt
```

6. **Run the development server**:

```bash
python manage.py runserver
```
The API should now be available at http://127.0.0.1:8000.

## Usage

### API Endpoints

| Endpoint                         | Method         | Description                                                     | Access Level            |
|----------------------------------|----------------|-----------------------------------------------------------------|-------------------------|
| `/auth/token/login/`            | `POST`         | Obtain an authentication token.                                 | All Users               |
| `/auth/users/`                  | `GET`          | List all users.                                                 | Manager Only            |
| `/auth/users/`                  | `POST`         | Register a new user (default to Customer role).                | All Users               |
| `/api/menu-items`              | `GET`          | List all menu items.                                          | All Users             |
| `/api/menu-items`              | `POST`         | Add a new menu item.                                          | Manager Only            |
| `/api/menu-items/{id}`         | `PUT`          | Update an existing menu item.                                 | Manager Only            |
| `/api/menu-items/{id}`         | `DELETE`       | Delete a menu item.                                          | Manager Only            |
| `/api/cart/menu-items`         | `GET`          | Retrieve items in the user's cart.                           | Customer Only           |
| `/api/cart/menu-items`         | `POST`         | Add a menu item to the cart.                                 | Customer Only           |
| `/api/cart/menu-items`         | `DELETE`       | Clear all items from the cart.                               | Customer Only           |
| `/api/orders`                  | `GET`          | Retrieve orders based on user role.                          | All Users               |
| `/api/orders`                  | `POST`         | Create a new order based on items in the cart (Customer only).| Customer Only           |
| `/api/orders/{id}`             | `GET`          | Retrieve order details.                                      | All Users               |
| `/api/orders/{id}`             | `PUT/PATCH`    | Update order details (Manager only) or status (Delivery Crew).| Manager/Delivery Crew   |
| `/api/orders/{id}`             | `DELETE`       | Delete an order (Manager only).                              | Manager Only            |
| `/api/manager/users`             | `GET`          | Retrieve all users in the Manager group.                        | Manager Only            |
| `/api/manager/users`             | `POST`         | Add a user to the Manager group.                                | Manager Only            |
| `/api/manager/users/{id}`        | `GET`          | Retrieve details of a specific Manager group user.              | Manager Only            |
| `/api/manager/users/{id}`        | `DELETE`       | Remove a user from the Manager group.                           | Manager Only            |
| `/api/delivery-crew/users`       | `GET`          | Retrieve all users in the Delivery Crew group.                  | Manager Only            |
| `/api/delivery-crew/users`       | `POST`         | Add a user to the Delivery Crew group.                          | Manager Only            |
| `/api/delivery-crew/users/{id}`  | `GET`          | Retrieve details of a specific Delivery Crew user.              | Manager Only            |
| `/api/delivery-crew/users/{id}`  | `DELETE`       | Remove a user from the Delivery Crew group.                     | Manager Only            |


### Sample Requests

### 1. Login

- **URL**: `/auth/token/login/`
- **Method**: `POST`
- **Description**: Authenticates users and generates a token.
- **Request Body**:
  ```json
  {
      "username": "admin",
      "password": "admin"
  }
  ```
- **Response**: Returns a access token upon successful authentication.


### 2. User registration

- **URL**: `/auth/users/`
- **Method**: `POST`
- **Description**: Creates a new user.
- **Request Body**:
  ```json
  {
      "username": "string",
      "password": "string",
      "email": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.


### 3. Users

- **URL**: `/auth/users/`
- **Method**: `GET`
- **Description**: Displays list of all user or current user.
- **Request Headers**: Requires a valid access token.
- **Response**: Returns a list of users in JSON format.


### 4. Menu items

#### A. Fetch All Menu Items (Basic Request)

- **URL**: `/api/menu-items`
- **Method**: `GET`
- **Query Params:** None
- **Description**: Displays list of menum items.
- **Response (200 OK):**
  ```json
  [
    {
        "id": 1,
        "title": "Cheesecake",
        "price": "5.99",
        "featured": true,
        "category": {
            "id": 1,
            "title": "Desserts",
            "slug": "desserts"
        }
    },
    {
        "id": 2,
        "title": "Chocolate Cake",
        "price": "4.99",
        "featured": true,
        "category": {
            "id": 1,
            "title": "Desserts",
            "slug": "desserts"
        }
    }
  ]
  ```

#### B. Filter by Category

- **URL**: `/api/menu-items?category=Appetizers`
- **Method**: `GET`
- **Response (200 OK):**
  ```json
  [
    {
        "id": 10,
        "title": "Bruschetta",
        "price": "6.99",
        "featured": true,
        "category": {
            "id": 4,
            "title": "Appetizers",
            "slug": "appetizers"
        }
    },
    {
        "id": 11,
        "title": "Garlic Bread",
        "price": "4.50",
        "featured": false,
        "category": {
            "id": 4,
            "title": "Appetizers",
            "slug": "appetizers"
        }
    }
  ]
  ```

#### C. Filter by Price

- **URL**: `/api/menu-items?price=4`
- **Method**: `GET`
- **Response (200 OK):**
  ```json
  [
    {
          "id": 4,
          "title": "Lemonade",
          "price": "2.50",
          "featured": true,
          "category": {
              "id": 2,
              "title": "Beverages",
              "slug": "beverages"
          }
      },
      {
          "id": 3,
          "title": "Apple Pie",
          "price": "3.99",
          "featured": false,
          "category": {
              "id": 1,
              "title": "Desserts",
              "slug": "desserts"
          }
      }
  ]
  ```

#### D. Search by Title

- **URL**: `/api/menu-items?search=Pancakes`
- **Method**: `GET`
- **Response (200 OK):**
  ```json
  [
    {
        "id": 20,
        "title": "Pancakes",
        "price": "6.99",
        "featured": true,
        "category": {
            "id": 1,
            "title": "Desserts",
            "slug": "desserts"
        }
    }
  ]
  ```

### E. Pagination

- **URL**: `/api/menu-items?page=3`
- **Method**: `GET`
- **Response (200 OK):**
  ```json
  [
    {
        "id": 21,
        "title": "Waffles",
        "price": "7.99",
        "featured": true,
        "category": {
            "id": 1,
            "title": "Desserts",
            "slug": "desserts"
        }
    },
    {
        "id": 22,
        "title": "Vegetable Stir Fry",
        "price": "9.99",
        "featured": false,
        "category": {
            "id": 3,
            "title": "Main",
            "slug": "main"
        }
    }
  ]
  ```

#### F. Add menu item

- **URL**: `/api/menu-items`
- **Method**: `POST`
- **Description**:Add a New Menu Item (Manager or Superuser).
- **Request Headers**: Requires a access token.
- **Request Body**:
  ```json
    {
      "title": "Cheeseburger",
      "price": 6.99,
      "featured": true,
      "category_id": 3
  }
  ```
- **Response (201 Created):**
  ```json
  {
      "id": 35,
      "title": "Cheeseburger",
      "price": 6.99,
      "featured": true,
      "category": {
        "id": 3,
        "title": "Main",
        "slug": "main"
    }
  }
  ```

#### G. Fetch Single Menu Item

- **URL**: `/api/menu-items/1`
- **Method**: `GET`
- **Query Params:** None
- **Description**: Displays Single menu item.
- **Response (200 OK):**
  ```json
    {
        "id": 1,
        "title": "Cheesecake",
        "price": "5.99",
        "featured": true,
        "category": {
            "id": 1,
            "title": "Desserts",
            "slug": "desserts"
    }
  ```

#### H. PUT Request Examples

- **URL**: `/api/menu-items/1`
- **Method**: `PUT`
- **Query Params:** None
- **Description**: Update Menu Item (Manager or Superuser).
- **Request Body:**
  ```json
    {
    "title": "Margherita Pizza - Extra Cheese",
    "price": "10.99",
    "featured": true,
    "category_id": 3
  }
  ```
- **Response (200 OK):**
  ```json
    {
    "id": 30,
    "title": "Margherita Pizza - Extra Cheese",
    "price": "10.99",
    "featured": true,
    "category": {
        "id": 3,
        "title": "Main",
        "slug": "main"
    }
  }
  ```

#### H. DELETE Menu Item

- **URL**: `/api/menu-items/1`
- **Method**: `DELETE`
- **Query Params:** None
- **Description**: Delete Menu Item (Manager or Superuser).
- **Response (204 No Content):**


### 5. Cart

#### A. Fetch All Items in Cart (Authorized User)

- **URL**: `/api/cart/menu-items`
- **Method**: `GET`
- **Description**: Displays list of All Items in Cart if current user already have items in the cart.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  [
   {
        "id": 13,
        "user": 5,
        "menuitems": {
            "id": 1,
            "title": "Cheesecake",
            "price": "5.99"
        },
        "quantity": 2,
        "unit_price": "5.99",
        "price": "11.98"
    },
    {
        "id": 14,
        "user": 5,
        "menuitems": {
            "id": 2,
            "title": "Chocolate Cake",
            "price": "4.99"
        },
        "quantity": 4,
        "unit_price": "4.99",
        "price": "19.96"
    }
  ]

#### B. Add Item to Cart (Authorized User)

- **URL**: `/api/cart/menu-items`
- **Method**: `POST`
- **Description**:Add Item to Cart for current user.
- **Request Headers**: Requires a access token.
- **Request Body**:
  ```json
  {
    "menuitems_id": 3,
    "quantity": 1
  }
  ```
- **Response (201 Created):**
  ```json
  {
      "id": 15,
      "user": 5,
      "menuitems": {
          "id": 3,
          "title": "Apple Pie",
          "price": "3.99"
      },
      "quantity": 1,
      "unit_price": "3.99",
      "price": "3.99"
  }
  ```

#### C. Delete All Items in Cart (Authorized User)

- **URL**: `/api/cart/menu-items`
- **Method**: `DELETE`
- **Description**: Successfully Delete All Items in Cart for the current user.
- **Response (204 No Content):**


### 6. Orders

#### A. Fetch All Orders depending on the role of the user like Customer, Delivery Crew, and Manager or Superuser.

- **URL**: `/api/orders`
- **Method**: `GET`
- **Description**: Displays list of All Orders.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  [
    {
        "id": 1,
        "user": 6,
        "delivery_crew": 4,
        "status": false,
        "total": "14.50",
        "date": "2024-10-19T12:22:16.149974Z",
        "orderitem_set": [
            {
                "id": 1,
                "menuitem": "Lemonade",
                "quantity": 4,
                "unit_price": "2.50",
                "price": "10.00"
            },
            {
                "id": 2,
                "menuitem": "Iced Tea",
                "quantity": 2,
                "unit_price": "2.25",
                "price": "4.50"
            }
        ]
    },
    {
        "id": 2,
        "user": 5,
        "delivery_crew": 7,
        "status": false,
        "total": "35.93",
        "date": "2024-10-19T13:18:06.683494Z",
        "orderitem_set": [
            {
                "id": 3,
                "menuitem": "Cheesecake",
                "quantity": 2,
                "unit_price": "5.99",
                "price": "11.98"
            },
            {
                "id": 4,
                "menuitem": "Chocolate Cake",
                "quantity": 4,
                "unit_price": "4.99",
                "price": "19.96"
            },
            {
                "id": 5,
                "menuitem": "Apple Pie",
                "quantity": 1,
                "unit_price": "3.99",
                "price": "3.99"
            }
        ]
    }
  ]
  ```

#### B. Fetch Only Pending or Delivered Orders by filtering

- **URL**: `/api/orders?status=pending`
- **URL**: `/api/orders?status=delivered`
- **Method**: `GET`
- **Description**: Displays list of All Orders based on the filter(only managers).
- **Query Params:** Yes
- **Request Headers**: Requires a access token.
- **Response (200 OK):**

#### C. Fetch Orders with Pagination

- **URL**: `/api/orders?page=2`
- **Method**: `GET`
- **Description**: Displays list of All Orders of the page 2 if there is or returns empty data.
- **Query Params:** Yes
- **Request Headers**: Requires a access token.
- **Response (200 OK):**

#### D. Create an Order (Only Authorized Customer)

 **URL**: `/api/orders`
- **Method**: `POST`
- **Description**:Successfully Creates an Order for current user.
- **Request Headers**: Requires a access token.
- **Request Body**: The body should be empty, you don't need to provide any data in the request body, the `POST` request for order creation retrieves items directly from the user's cart.
- **Response (201 Created):**

#### E. Manager Updating Order Details using PUT or PATCH Requests.

- **URL**: `/api/orders/1`
- **Method**: `PUT` or 'PATCH'
- **Query Params:** None
- **Description**: Update status of the Order or assign to delivery crew (Manager or Superuser).
- **Request Body:**
  ```json
  {
    "delivery_crew": 7,
    "status": true
  }
  ```
- **Response (200 OK):**

#### F. Delivery Crew Member Updating Only the Order Status.

- **URL**: `/api/orders/1`
- **Method**: `PUT` or 'PATCH'
- **Query Params:** None
- **Description**: Updates the status of the Order.
- **Request Body:**
  ```json
  {
    "status": true
  }
  ```
- **Response (200 OK):**


### 7. Managers group

#### A. Fetch All Managers(Manager or Superuser)

- **URL**: `/api/groups/manager/users`
- **Method**: `GET`
- **Description**: Displays list of All Users in the Manager group.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  [
     {
        "id": 2,
        "username": "johndoe",
        "email": "john@little.lemon",
        "date_joined": "2024-10-15"
    },
    {
        "id": 3,
        "username": "janedoe",
        "email": "jane@little.lemon",
        "date_joined": "2024-10-15"
    }
  ]
  ```

  #### B. Get single managaer user(Manager or Superuser)

- **URL**: `/api/groups/manager/users/1`
- **Method**: `GET`
- **Description**: Displays a single user in the Manager group.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  {
      "id": 2,
      "username": "johndoe",
      "email": "john@little.lemon",
      "date_joined": "2024-10-15"
  }
  ```

#### C. Add user to the manager group

 **URL**: `/api/groups/manager/users`
- **Method**: `POST`
- **Description**:Successfully Adds a user to the manager group.
- **Request Headers**: Requires a access token.
- **Request Body**:
```json
{
  "id": 3
}
```
- **Response (201 Created):**

#### D. Remove user from manager group

 **URL**: `/api/groups/manager/users/2`
- **Method**: `DELETE`
- **Description**:Removes a user from manager group.
- **Request Headers**: Requires a access token.
- **Response (- 204 No Content):**


### 8. Delivery crew group

#### A. Fetch All Delivery crews(Manager or Superuser)

- **URL**: `/api/groups/delivery-crew/users`
- **Method**: `GET`
- **Description**: Displays list of All Users in the Delivery crew group.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  [
     {
        "id": 4,
        "username": "mikedoe",
        "email": "mike@little.lemon",
        "date_joined": "2024-10-15"
    },
    {
        "id": 7,
        "username": "alexdoe",
        "email": "alex@little.lemon",
        "date_joined": "2024-10-16"
    }
  ]
  ```

  #### B. Get single Delivery crew(Manager or Superuser)

- **URL**: `/api/groups/manager/users/1`
- **Method**: `GET`
- **Description**: Displays a single user in the Delivery crew group.
- **Request Headers**: Requires a access token.
- **Response (200 OK):**
  ```json
  {
      "id": 4,
      "username": "mikedoe",
      "email": "mike@little.lemon",
      "date_joined": "2024-10-15"
  }
  ```

#### C. Add user to the Delivery crew group

 **URL**: `/api/groups/manager/users`
- **Method**: `POST`
- **Description**:Successfully Adds a user to the manager group.
- **Request Headers**: Requires a access token.
- **Request Body**:
```json
{
  "id": 2
}
```
- **Response (201 Created):**

#### D. Remove user from manager group

 **URL**: `/api/groups/manager/users/2`
- **Method**: `DELETE`
- **Description**:Removes a user from manager group.
- **Request Headers**: Requires a access token.
- **Response (- 204 No Content):**


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
