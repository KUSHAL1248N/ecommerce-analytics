import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("python_app")

from db_connection import create_connection


# Connect to MySQL
connection = create_connection()

query = """
    SELECT
        product_name,
        revenue
    FROM product_performance
    ORDER BY revenue DESC
    LIMIT 5
"""

df = pd.read_sql(query, connection)

connection.close()


# Display data
print(df)


# Create chart
plt.figure(figsize=(10, 5))

plt.bar(
    df["product_name"],
    df["revenue"]
)

plt.title("Top 5 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=30, ha="right")

plt.tight_layout()

plt.show()