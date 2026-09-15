import os
import sys

import pandas as pd

sys.path.append("python_app")

from db_connection import create_connection


# Create output folder if it doesn't exist
output_folder = "powerbi_data"
os.makedirs(output_folder, exist_ok=True)


# Connect to MySQL
connection = create_connection()


# Views to export
views = {
    "customer_count": "SELECT COUNT(*) AS total_customers FROM customers",

    "order_status": """
        SELECT
            status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY status
        ORDER BY order_count DESC
    """,
    
    "aov": """
        SELECT
            ROUND(SUM(total_amount) / COUNT(*), 2) AS average_order_value
        FROM orders
        WHERE status = 'Delivered'
    """,

    "monthly_revenue": "SELECT * FROM monthly_revenue ORDER BY month",
    "customer_lifetime_value": """
        SELECT *
        FROM customer_lifetime_value
        ORDER BY lifetime_value DESC
    """,
    "product_performance": """
        SELECT *
        FROM product_performance
        ORDER BY revenue DESC
    """,
    "seller_performance": """
        SELECT *
        FROM seller_performance
        ORDER BY profit DESC
    """
}


# Export each view
for filename, query in views.items():

    df = pd.read_sql(query, connection)

    file_path = os.path.join(
        output_folder,
        f"{filename}.csv"
    )

    df.to_csv(file_path, index=False)

    print(f"Exported: {file_path}")
    print(f"Rows: {len(df)}")
    print()


# Close connection
connection.close()

print("All Power BI data exported successfully!")