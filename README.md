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

### Login

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

### User registration

- **URL**: `/auth/users`
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


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
