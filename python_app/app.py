from db_connection import create_connection


# Create database connection
connection = create_connection()
cursor = connection.cursor()


# -----------------------------
# Business Overview
# -----------------------------
def business_overview():
    print("\n========================================")
    print("           BUSINESS OVERVIEW")
    print("========================================")

    queries = {
        "Total Customers": "SELECT COUNT(*) FROM customers",
        "Total Products": "SELECT COUNT(*) FROM products",
        "Total Orders": "SELECT COUNT(*) FROM orders",
        "Delivered Orders": """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'Delivered'
        """,
        "Total Revenue": """
            SELECT SUM(total_amount)
            FROM orders
            WHERE status = 'Delivered'
        """,
        "Average Order Value": """
            SELECT ROUND(AVG(total_amount), 2)
            FROM orders
            WHERE status = 'Delivered'
        """
    }

    for name, query in queries.items():
        cursor.execute(query)
        result = cursor.fetchone()[0]

        if result is None:
            result = 0

        if name in ["Total Revenue", "Average Order Value"]:
            print(f"{name:<25}: ₹{result:,.2f}")
        else:
            print(f"{name:<25}: {result}")


# -----------------------------
# Top Customers
# -----------------------------
def top_customers():
    print("\n========================================")
    print("             TOP CUSTOMERS")
    print("========================================")

    query = """
        SELECT
            customer_name,
            total_orders,
            lifetime_value
        FROM customer_lifetime_value
        ORDER BY lifetime_value DESC
        LIMIT 5
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"{'Customer':<20} {'Orders':<10} {'Spent':>12}")
    print("-" * 45)

    for customer, orders, spent in results:
        print(f"{customer:<20} {orders:<10} ₹{spent:>10,.2f}")


# -----------------------------
# Top Products
# -----------------------------
def top_products():
    print("\n========================================")
    print("              TOP PRODUCTS")
    print("========================================")

    query = """
        SELECT
            product_name,
            units_sold,
            revenue,
            profit
        FROM product_performance
        ORDER BY revenue DESC
        LIMIT 5
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"{'Product':<25} {'Units':>8} {'Revenue':>16} {'Profit':>16}")
    print("-" * 70)

    for product, units, revenue, profit in results:
        print(
            f"{product:<25} "
            f"{units:>8} "
            f"{'₹' + format(revenue, ',.2f'):>16} "
            f"{'₹' + format(profit, ',.2f'):>16}"
        )


# -----------------------------
# Seller Performance
# -----------------------------
def seller_performance():
    print("\n========================================")
    print("          SELLER PERFORMANCE")
    print("========================================")

    query = """
        SELECT
            seller_name,
            total_orders,
            revenue,
            profit
        FROM seller_performance
        ORDER BY profit DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(
        f"{'Seller':<20}"
        f"{'Orders':<8}"
        f"{'Revenue':>12}"
        f"{'Profit':>12}"
    )
    print("-" * 55)

    for seller, orders, revenue, profit in results:
        print(
            f"{seller:<20}"
            f"{orders:<8}"
            f"₹{revenue:>10,.2f}"
            f"₹{profit:>10,.2f}"
        )

# -----------------------------
# Category Performance
# -----------------------------
def category_performance():
    print("\n========================================")
    print("         CATEGORY PERFORMANCE")
    print("========================================")

    query = """
        SELECT
            c.category_name,
            SUM(oi.quantity * oi.unit_price) AS revenue
        FROM categories c
        JOIN products p
            ON c.category_id = p.category_id
        JOIN order_items oi
            ON p.product_id = oi.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'Delivered'
        GROUP BY c.category_id, c.category_name
        ORDER BY revenue DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"{'Category':<20}{'Revenue':>15}")
    print("-" * 35)

    for category, revenue in results:
        print(f"{category:<20}₹{revenue:>13,.2f}")

# -----------------------------
# Order Status Analysis
# -----------------------------
def order_status_analysis():
    print("\n========================================")
    print("          ORDER STATUS ANALYSIS")
    print("========================================")

    query = """
        SELECT
            status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY status
        ORDER BY order_count DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"{'Status':<20}{'Orders':>10}")
    print("-" * 30)

    for status, order_count in results:
        print(f"{status:<20}{order_count:>10}")

# -----------------------------
# Monthly Revenue
# -----------------------------
def monthly_revenue():
    print("\n========================================")
    print("            MONTHLY REVENUE")
    print("========================================")

    query = """
        SELECT
            month,
            total_orders,
            revenue
        FROM monthly_revenue
        ORDER BY month
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(
        f"{'Month':<12}"
        f"{'Orders':<10}"
        f"{'Revenue':>15}"
    )
    print("-" * 40)

    for month, orders, revenue in results:
        print(
            f"{month:<12}"
            f"{orders:<10}"
            f"₹{revenue:>13,.2f}"
        )

# -----------------------------
# Customer Search
# -----------------------------
def customer_search():
    print("\n========================================")
    print("            CUSTOMER SEARCH")
    print("========================================")

    name = input("Enter customer name: ").strip()

    query = """
        SELECT
            customer_name,
            city,
            total_orders,
            lifetime_value
        FROM customer_lifetime_value
        WHERE customer_name LIKE %s
    """

    cursor.execute(query, (f"%{name}%",))
    results = cursor.fetchall()

    if not results:
        print("\nNo customer found.")
        return

    print()

    for customer, city, orders, lifetime_value in results:
        print(f"Customer       : {customer}")
        print(f"City           : {city}")
        print(f"Total Orders   : {orders}")
        print(f"Lifetime Value : ₹{lifetime_value:,.2f}")
        print("----------------------------------------")

# -----------------------------
# Product Search
# -----------------------------
def product_search():
    print("\n========================================")
    print("             PRODUCT SEARCH")
    print("========================================")

    name = input("Enter product name: ").strip()

    query = """
        SELECT
            product_name,
            category_name,
            seller_name,
            units_sold,
            revenue,
            profit
        FROM product_performance
        WHERE product_name LIKE %s
    """

    cursor.execute(query, (f"%{name}%",))
    results = cursor.fetchall()

    if not results:
        print("\nNo product found.")
        return

    print()

    for product, category, seller, units, revenue, profit in results:
        print(f"Product       : {product}")
        print(f"Category      : {category}")
        print(f"Seller        : {seller}")
        print(f"Units Sold    : {units}")
        print(f"Revenue       : ₹{revenue:,.2f}")
        print(f"Profit        : ₹{profit:,.2f}")
        print("----------------------------------------")

# -----------------------------
# Order Search
# -----------------------------
def order_search():
    print("\n========================================")
    print("              ORDER SEARCH")
    print("========================================")

    order_id = input("Enter order ID: ").strip()

    if not order_id.isdigit():
        print("\nPlease enter a valid numeric order ID.")
        return

    query = """
        SELECT
            o.order_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            o.order_date,
            o.status,
            o.total_amount,
            p.payment_method,
            p.payment_status
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        LEFT JOIN payments p
            ON o.order_id = p.order_id
        WHERE o.order_id = %s
    """

    cursor.execute(query, (int(order_id),))
    result = cursor.fetchone()

    if not result:
        print("\nNo order found.")
        return

    (
        order_id,
        customer,
        order_date,
        status,
        total_amount,
        payment_method,
        payment_status
    ) = result

    print()
    print(f"Order ID       : {order_id}")
    print(f"Customer       : {customer}")
    print(f"Order Date     : {order_date}")
    print(f"Status         : {status}")
    print(f"Total Amount   : ₹{total_amount:,.2f}")
    print(f"Payment Method : {payment_method}")
    print(f"Payment Status : {payment_status}")
    print("----------------------------------------")


# -----------------------------
# Main Menu
# -----------------------------
while True:

    print("\n")
    print("========================================")
    print("       E-COMMERCE ANALYTICS SYSTEM")
    print("========================================")
    print("1. Business Overview")
    print("2. Top Customers")
    print("3. Top Products")
    print("4. Seller Performance")
    print("5. Monthly Revenue")
    print("6. Category Performance")
    print("7. Order Status Analysis")
    print("8. Customer Search")
    print("9. Product Search")
    print("10. Order Search")
    print("11. Exit")
    print("========================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        business_overview()

    elif choice == "2":
        top_customers()

    elif choice == "3":
        top_products()

    elif choice == "4":
        seller_performance()

    elif choice == "5":
        monthly_revenue()

    elif choice == "6":
        category_performance()

    elif choice == "7":
        order_status_analysis()

    elif choice == "8":
        customer_search()

    elif choice == "9":
        product_search()

    elif choice == "10":
        order_search()

    elif choice == "11":
        print("\nThank you for using E-Commerce Analytics System!")
        break

    else:
        print("\nInvalid choice. Please enter a number from 1 to 11.")


# -----------------------------
# Close Connection
# -----------------------------
cursor.close()
connection.close()