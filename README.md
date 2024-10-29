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
      "price": 8.49,
      "category": 3
  }
  ```
- **Response (201 Created):**
  ```json
  {
      "id": 32,
      "title": "Cheeseburger",
      "price": 8.49,
      "category": {
        "id": 3,
        "title": "Burger"
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

#### H. DELETE Request Examples

- **URL**: `/api/menu-items/1`
- **Method**: `DELETE`
- **Query Params:** None
- **Description**: Delete Menu Item (Manager or Superuser).
- **Response (204 No Content):**

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
