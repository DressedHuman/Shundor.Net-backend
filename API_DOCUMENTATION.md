# Shundor.Net Backend API Documentation

## Overview
E-commerce backend API built with Django REST Framework featuring product management, shopping cart, orders, reviews, and user authentication.

**Repository**: [DressedHuman/Shundor.Net-backend](https://github.com/DressedHuman/Shundor.Net-backend)  
**Base URL**: `http://localhost:8000`

---

## Quick Start

### Authentication
The API uses **JWT (primary)** and **Token-based** authentication via Djoser with **phone number** as the login identifier.

**Important**: 
- Login field is `phone_number` (not email)
- Phone format: E.164 (e.g., `+8801712345678` for Bangladesh)
- JWT access tokens are valid for **7 days**
- JWT refresh tokens are valid for **30 days**

#### Register
```http
POST /auth/users/
Content-Type: application/json

{
  "phone_number": "+8801712345678",
  "email": "user@example.com",
  "password": "securepassword",
  "profile": {
    "first_name": "John",
    "last_name": "Doe"
  }
}

Response:
{
  "id": 1,
  "phone_number": "+8801712345678",
  "email": "user@example.com",
  "is_verified": true,
  "profile": {
    "id": 1,
    "user_type": "customer",
    "first_name": "John",
    "last_name": "Doe",
    ...
  }
}
```

#### Login (JWT - PRIMARY METHOD)
```http
POST /auth/jwt/create/
Content-Type: application/json

{
  "phone_number": "+8801712345678",
  "password": "securepassword"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh JWT Token
```http
POST /auth/jwt/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login (Token - Alternative)
```http
POST /auth/token/login/
Content-Type: application/json

{
  "phone_number": "+8801712345678",
  "password": "securepassword"
}

Response:
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### Get Current User
```http
GET /auth/users/me/
Authorization: Bearer <jwt-access-token>

Response:
{
  "id": 1,
  "phone_number": "+8801712345678",
  "email": "user@example.com",
  "is_verified": true,
  "is_active": true,
  "is_staff": false,
  "date_joined": "2025-12-01T10:00:00Z",
  "profile": {
    "id": 1,
    "user_type": "customer",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+8801712345678",
    "email": "user@example.com",
    "is_verified": true,
    "date_of_birth": null,
    "gender": null,
    "profile_image": null,
    "default_shipping_address": null,
    "default_billing_address": null,
    "modified_at": "2025-12-01T10:00:00Z"
  }
}
```

#### Use Authentication
Include in headers:
```
# JWT (Primary)
Authorization: Bearer <your-jwt-access-token>

# OR Token (Alternative)
Authorization: Token <your-auth-token>
```

---

## API Endpoints

### Products

#### List Products
```http
GET /products/
```
Returns paginated list of products with images, sizes, colors, and reviews.

#### Get Product Details
```http
GET /products/{id}/
```

#### Create Product (Admin)
```http
POST /products/create/
Content-Type: multipart/form-data
Authorization: Token <admin-token>

{
  "name": "T-Shirt",
  "slug": "t-shirt",
  "category": 1,
  "brand": 1,
  "description": "Cotton T-Shirt",
  "sku": "TSH001",
  "price": "29.99",
  "old_price": "39.99",
  "stock": 100,
  "size_ids": [1, 2, 3],
  "color_ids": [1, 4, 5],
  "images": "[{\"alt_text\": \"Front view\", \"is_primary\": true, \"order\": 0}]",
  "image_0": <file>
}
```

#### Update Product (Admin)
```http
PUT /products/{id}/update/
PATCH /products/{id}/update/
```

---

### Sizes

#### List Sizes
```http
GET /sizes/
```

#### Create Size (Admin)
```http
POST /sizes/
Content-Type: application/json
Authorization: Token <admin-token>

{
  "name": "Medium",
  "code": "M",
  "order": 2,
  "is_active": true
}
```

#### Update/Delete Size (Admin)
```http
PUT /sizes/{id}/update/
PATCH /sizes/{id}/update/
DELETE /sizes/{id}/delete/
```

---

### Colors

#### List Colors
```http
GET /colors/
```

#### Create Color (Admin)
```http
POST /colors/
Content-Type: application/json
Authorization: Token <admin-token>

{
  "name": "Red",
  "hex_code": "#FF0000",
  "is_active": true
}
```

#### Update/Delete Color (Admin)
```http
PUT /colors/{id}/update/
PATCH /colors/{id}/update/
DELETE /colors/{id}/delete/
```

---

### Cart

#### Get Cart
```http
GET /cart/
Authorization: Token <your-token>
```

#### Add to Cart
```http
POST /items/
Content-Type: application/json
Authorization: Token <your-token>

{
  "product_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```http
PATCH /items/{id}/
Content-Type: application/json
Authorization: Token <your-token>

{
  "quantity": 3
}
```

#### Remove from Cart
```http
DELETE /items/{id}/delete/
Authorization: Token <your-token>
```

---

### Orders

#### Create Order
```http
POST /orders/
Content-Type: application/json
Authorization: Token <your-token>

{
  "shipping_address": "123 Main St, City, Country",
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}
```

#### Get Order History
```http
GET /order-history/
Authorization: Token <your-token>
```

#### Get Order Details
```http
GET /orders/{id}/
Authorization: Token <your-token>
```

#### Update Order Status (Admin)
```http
POST /orders/{id}/update-status/
Content-Type: application/json
Authorization: Token <admin-token>

{
  "status": "shipped"
}
```

**Status Options**: `pending`, `processing`, `shipped`, `delivered`, `cancelled`

---

### Reviews

#### List Reviews
```http
GET /reviews/
```

#### Create Review
```http
POST /reviews/
Content-Type: application/json
Authorization: Token <your-token>

{
  "product": 1,
  "rating": 5,
  "comment": "Great product!"
}
```

#### Update/Delete Review
```http
PUT /reviews/{id}/
PATCH /reviews/{id}/
DELETE /reviews/{id}/
Authorization: Token <your-token>
```

---

### Wishlist

#### Get Wishlist
```http
GET /wishlist/
Authorization: Token <your-token>
```

#### Add to Wishlist
```http
POST /wishlist/
Content-Type: application/json
Authorization: Token <your-token>

{
  "product": 1
}
```

#### Remove from Wishlist
```http
DELETE /wishlist/{id}/
Authorization: Token <your-token>
```

---

### Categories

#### List Categories
```http
GET /categories/
```

#### Create Category (Admin)
```http
POST /categories/create/
Content-Type: multipart/form-data
Authorization: Token <admin-token>

{
  "name": "Electronics",
  "image": <file>,
  "is_active": true
}
```

#### Update/Delete Category (Admin)
```http
PUT /categories/{id}/update/
PATCH /categories/{id}/update/
DELETE /categories/{id}/delete/
```

---

### Brands

#### List Brands
```http
GET /brands/
```

#### Create Brand (Admin)
```http
POST /brands/create/
Content-Type: multipart/form-data
Authorization: Token <admin-token>

{
  "name": "Nike",
  "logo": <file>,
  "is_active": true
}
```

#### Update/Delete Brand (Admin)
```http
PUT /brands/{id}/update/
PATCH /brands/{id}/update/
DELETE /brands/{id}/delete/
```

---

### Banners

#### Get Active Banners
```http
GET /banner/get_all_active_banners/
```

#### Get All Banners (Admin)
```http
GET /banner/get_all_banners/
Authorization: Token <admin-token>
```

#### Create Banner (Admin)
```http
POST /banner/add_banner/
Content-Type: multipart/form-data
Authorization: Token <admin-token>

{
  "title": "Summer Sale",
  "image": <file>,
  "link": "/products/sale",
  "is_published": true
}
```

---

### Contact

#### Submit Contact Form
```http
POST /contacts/create/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Question",
  "message": "I have a question about..."
}
```

#### List Contacts (Admin)
```http
GET /contacts/
Authorization: Token <admin-token>
```

---

### Shipping Charges

#### List Shipping Charges
```http
GET /shipping-charges/
```

#### Create Shipping Charge (Admin)
```http
POST /shipping-charges/
Content-Type: application/json
Authorization: Token <admin-token>

{
  "region": "Dhaka",
  "charge": "60.00",
  "is_active": true
}
```

---

### Site Settings

#### Get Site Settings
```http
GET /site-settings/
```

#### Update Site Setting (Admin)
```http
PATCH /site-settings/{id}/
Content-Type: application/json
Authorization: Token <admin-token>

{
  "value": "new-value"
}
```

---

## Data Models

### Product
```json
{
  "id": 1,
  "name": "T-Shirt",
  "slug": "t-shirt",
  "category": 1,
  "category_name": "Clothing",
  "brand": 1,
  "brand_name": "Nike",
  "description": "Cotton T-Shirt",
  "sku": "TSH001",
  "old_price": "39.99",
  "price": "29.99",
  "stock": 100,
  "is_active": true,
  "created_at": "2025-12-01T00:00:00Z",
  "updated_at": "2025-12-01T00:00:00Z",
  "images": [
    {
      "id": 1,
      "image": "/media/products/tshirt.jpg",
      "alt_text": "Front view",
      "is_primary": true,
      "order": 0
    }
  ],
  "sizes": [
    {
      "id": 1,
      "name": "Small",
      "code": "S",
      "order": 1,
      "is_active": true
    }
  ],
  "colors": [
    {
      "id": 1,
      "name": "Red",
      "hex_code": "#FF0000",
      "is_active": true
    }
  ],
  "reviews": []
}
```

### Cart
```json
{
  "id": 1,
  "user": 1,
  "created_at": "2025-12-01T00:00:00Z",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "T-Shirt",
        "price": "29.99",
        "images": [...]
      },
      "quantity": 2
    }
  ]
}
```

### Order
```json
{
  "id": 1,
  "user": 1,
  "status": "pending",
  "total_amount": "59.98",
  "shipping_address": "123 Main St",
  "customer_name": "John Doe",
  "customer_phone": "+1234567890",
  "created_at": "2025-12-01T00:00:00Z",
  "updated_at": "2025-12-01T00:00:00Z",
  "items": [
    {
      "id": 1,
      "product": 1,
      "quantity": 2,
      "price": "29.99"
    }
  ]
}
```

---

## Common Response Formats

### Pagination
```json
{
  "count": 100,
  "next": "http://localhost:8000/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "field_name": ["This field is required."]
}
```

#### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Recent Changes

### Version 1.0.0 (December 2025)

1. **Removed ProductVariant Model**
   - Products now have direct `price`, `stock`, and `sku` fields
   - Simplified product structure

2. **Added ProductImage Model**
   - Support for multiple images per product
   - Each image has `alt_text`, `is_primary`, and `order` fields

3. **Added Size and Color Models**
   - Separate models for sizes and colors
   - ManyToMany relationships with Product
   - Products can have multiple sizes and colors

4. **Updated Cart and Order**
   - Now reference `Product` directly instead of `ProductVariant`
   - Simplified order processing

---

## Admin Panel

Access the Django admin panel at:
```
http://localhost:8000/admin/
```

Default superuser credentials (development):
- **Username**: admin
- **Password**: admin123

---

## Development Notes

- **Media Files**: Served from `/media/` when `DEBUG=True`
- **Pagination**: Default page size is 10-20 items
- **Filtering**: Use query parameters like `?category=1&brand=2`
- **Ordering**: Use `?ordering=-created_at` for descending order

---

## Testing Examples

### cURL Examples

#### Get Products
```bash
curl http://localhost:8000/products/
```

#### Register
```bash
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number":"+8801712345678",
    "email":"user@example.com",
    "password":"password"
  }'
```

#### Login (JWT)
```bash
curl -X POST http://localhost:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number":"+8801712345678",
    "password":"password"
  }'
```

#### Login (Token)
```bash
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number":"+8801712345678",
    "password":"password"
  }'
```

#### Add to Cart
```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token-here" \
  -d '{
    "product_id":1,
    "quantity":2
  }'
```

### JavaScript/Fetch Examples

#### Get Products
```javascript
fetch('http://localhost:8000/products/')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### Register
```javascript
fetch('http://localhost:8000/auth/users/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone_number: '+8801712345678',
    email: 'user@example.com',
    password: 'password'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### Login (JWT)
```javascript
fetch('http://localhost:8000/auth/jwt/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone_number: '+8801712345678',
    password: 'password'
  })
})
.then(response => response.json())
.then(data => {
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
});
```

#### Login (Token)
```javascript
fetch('http://localhost:8000/auth/token/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone_number: '+8801712345678',
    password: 'password'
  })
})
.then(response => response.json())
.then(data => {
  localStorage.setItem('token', data.auth_token);
});
```

#### Add to Cart (Authenticated with JWT)
```javascript
const accessToken = localStorage.getItem('access_token');

fetch('http://localhost:8000/items/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    product_id: 1,
    quantity: 2
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### Add to Cart (Authenticated with Token)
```javascript
const token = localStorage.getItem('token');

fetch('http://localhost:8000/items/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  },
  body: JSON.stringify({
    product_id: 1,
    quantity: 2
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/DressedHuman/Shundor.Net-backend).
