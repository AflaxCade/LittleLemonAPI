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

#### Authentication
- **POST /api/auth/login/**: Obtain an authentication token.
- **POST /api/auth/register/**: Register a new user (default to Customer role).

#### Menu Management (Manager Only)
- **GET /api/menu-items/**: List all menu items.
- **POST /api/menu-items/**: Add a new menu item.
- **PUT /api/menu-items/{id}/**: Update an existing menu item.
- **DELETE /api/menu-items/{id}/**: Delete a menu item.

#### Cart Management (Customer Only)
- **GET /api/cart/menu-items/**: Retrieve items in the user's cart.
- **POST /api/cart/menu-items/**: Add a menu item to the cart.
- **DELETE /api/cart/menu-items/**: Clear all items from the cart.

#### Order Management
- **GET /api/orders/**: Retrieve orders based on user role.
  - **Managers**: View all orders.
  - **Delivery Crew**: View assigned orders.
  - **Customers**: View own orders.
- **POST /api/orders/**: Create a new order based on items in the cart (Customer only).
- **GET /api/orders/{id}/**: Retrieve order details.
- **PUT/PATCH /api/orders/{id}/**: Update order details (Manager only) or status (Delivery Crew).
- **DELETE /api/orders/{id}/**: Delete an order (Manager only).


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
