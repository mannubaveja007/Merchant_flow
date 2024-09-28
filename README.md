# 🛒 Merchant Dashboard API Documentation

Hello there! Welcome to the **Merchant Dashboard API Documentation**. This project enables merchants to manage payments, products, subscriptions, and more by integrating with PayME for secure transactions.

## Overview 📚

The Merchant Dashboard allows merchants to handle various aspects of their business, such as authentication, product management, invoicing, and payments. Each section is designed with security features like JWT authentication to ensure secure transactions.

## API Endpoints 🚀

### Authentication 🔑

- **Register**: `POST /auth/register`  
  Registers a new merchant.  
  - Request:  
    ```json
    { "username": "your_username", "password": "your_password" }
    ```
  - Response:  
    - `201 Created` 
    - `400 Bad Request`

- **Login**: `POST /auth/login`  
  Authenticates a merchant and returns a JWT token.  
  - Request:  
    ```json
    { "username": "your_username", "password": "your_password" }
    ```
  - Response:  
    - `200 OK (with JWT token)` 
    - `401 Unauthorized`

### Product Management 📦

- **Create Product**: `POST /products`  
  Adds a new product to the merchant's inventory.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Request:  
    ```json
    { "name": "Sample Product", "price": 29.99, "quantity": 100 }
    ```
  - Response:  
    - `201 Created`

- **Get Product**: `GET /products/<product_id>`  
  Retrieves details of a specific product.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Response:  
    - `200 OK`
    - `404 Not Found`

- **Update Product**: `PUT /products/<product_id>`  
  Updates a product’s details.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Request:  
    ```json
    { "price": 24.99, "quantity": 80 }
    ```
  - Response:  
    - `200 OK`
    - `404 Not Found`

- **Delete Product**: `DELETE /products/<product_id>`  
  Removes a product from inventory.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Response:  
    - `200 OK`
    - `404 Not Found`

### Invoice Management 📄

- **Create Invoice**: `POST /invoices`  
  Generates an invoice for a customer.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Request:  
    ```json
    { "customer_name": "John Doe", "amount_due": 150.00, "due_date": "2024-10-15" }
    ```
  - Response:  
    - `201 Created`

- **Get Invoice**: `GET /invoices/<invoice_id>`  
  Fetches a specific invoice's details.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Response:  
    - `200 OK`
    - `404 Not Found`

- **Update Invoice**: `PUT /invoices/<invoice_id>`  
  Modifies invoice details like amount or status.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Request:  
    ```json
    { "amount_due": 175.00, "status": "paid" }
    ```
  - Response:  
    - `200 OK`
    - `404 Not Found`

- **Delete Invoice**: `DELETE /invoices/<invoice_id>`  
  Deletes an invoice.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Response:  
    - `200 OK`
    - `404 Not Found`

### Payment Management 💸

- **Transfer Money**: `POST /payments/transfer`  
  Initiates a payment transfer.  
  - Header:  
    `Authorization: Bearer <your_jwt_token>`
  - Request:  
    ```json
    { "amount": 50, "to_account": "<recipient_account>" }
    ```
  - Response:  
    - `200 OK`
    - Error message

## Security Features 🛡️

- **Two-Factor Authentication (2FA)**
- **IP Whitelisting**
- **Login Activity Tracking**

---

## Conclusion 🎉

This API provides the necessary endpoints for managing a merchant's operations effectively. Use these endpoints to integrate payment processing, product management, and invoicing into your applications. 

**Happy Coding!** 🎉
