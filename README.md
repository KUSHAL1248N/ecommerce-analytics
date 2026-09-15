# E-Commerce Sales & Customer Analytics System

An end-to-end e-commerce analytics project built using **MySQL, Python, SQL, and Power BI** to analyze sales performance, customer behavior, product performance, seller profitability, and order trends.

## Project Overview

This project simulates an e-commerce business analytics system.

The system stores transactional data in a relational MySQL database, performs business analysis using SQL, provides an interactive Python application for querying business insights, generates analytical charts using Python, and presents key insights through an interactive Power BI dashboard.

### Data Flow

MySQL Database
        ↓
SQL Analysis & Views
        ↓
Python Application
        ↓
Python Data Export
        ↓
CSV Files
        ↓
Power BI Dashboard

## Technologies Used

- **MySQL** — Relational database and data storage
- **SQL** — Data analysis, joins, aggregations, subqueries, CTEs, window functions, and views
- **Python** — Interactive analytics application and data processing
- **Pandas** — Data analysis and CSV generation
- **Matplotlib** — Data visualization
- **Power BI** — Interactive business intelligence dashboard
- **VS Code** — Development environment
- **Git & GitHub** — Version control and project hosting

## Database Design

The MySQL database is named:

`ecommerce_analytics`

It contains 9 relational tables:

1. `customers`
2. `categories`
3. `sellers`
4. `products`
5. `inventory`
6. `orders`
7. `order_items`
8. `payments`
9. `reviews`

The database uses primary keys and foreign keys to maintain relationships between customers, orders, products, sellers, payments, and reviews.

## Dataset

The project contains:

- **20 customers**
- **8 categories**
- **8 sellers**
- **29 products**
- **29 inventory records**
- **45 orders**
- **52 order items**
- **45 payments**
- **40 reviews**

Order status distribution:

| Status | Orders |
|---|---:|
| Delivered | 36 |
| Shipped | 5 |
| Cancelled | 4 |

## SQL Analysis

The `analysis/` directory contains SQL scripts for different analytical tasks.

### Basic Business Analysis

Analyzes:

- Total customers
- Total products
- Total orders
- Delivered orders
- Delivered revenue
- Average order value
- Items sold

### Customer Analysis

Analyzes:

- Customer lifetime value
- Top customers
- Repeat customers
- Customers without delivered orders
- Average order value by customer

### Product Analysis

Analyzes:

- Units sold
- Product revenue
- Top products
- Category revenue
- Product ratings
- Low-stock products

### Seller & Profit Analysis

Analyzes:

- Seller revenue
- Seller profit
- Product-level profit
- Profit margins
- Seller performance

### Advanced Analysis

Uses advanced SQL techniques for:

- Monthly revenue analysis
- Customer ranking
- Product ranking
- Top product by category
- Month-over-month revenue changes

### SQL Views

The project creates reusable views:

- `monthly_revenue`
- `customer_lifetime_value`
- `product_performance`
- `seller_performance`

These views are also used by the Python application and Power BI data pipeline.

## Python Application

The project includes an interactive command-line analytics application.

Run it using:

```bash
py python_app/app.py