import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("python_app")

from db_connection import create_connection


# Connect to MySQL
connection = create_connection()

query = """
    SELECT
        category_name,
        revenue
    FROM (
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
    ) AS category_sales
    ORDER BY revenue DESC
"""

df = pd.read_sql(query, connection)

connection.close()


print(df)


# Create chart
plt.figure(figsize=(10, 5))

plt.bar(
    df["category_name"],
    df["revenue"]
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()