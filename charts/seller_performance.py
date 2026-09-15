import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("python_app")

from db_connection import create_connection


# Connect to MySQL
connection = create_connection()

query = """
    SELECT
        seller_name,
        revenue,
        profit
    FROM seller_performance
    ORDER BY revenue DESC
"""

df = pd.read_sql(query, connection)

connection.close()


# Display data
print(df)


# Create chart
plt.figure(figsize=(10, 5))

x = range(len(df))

plt.bar(
    [i - 0.2 for i in x],
    df["revenue"],
    width=0.4,
    label="Revenue"
)

plt.bar(
    [i + 0.2 for i in x],
    df["profit"],
    width=0.4,
    label="Profit"
)

plt.xticks(x, df["seller_name"], rotation=30, ha="right")

plt.title("Seller Revenue vs Profit")
plt.xlabel("Seller")
plt.ylabel("Amount (₹)")
plt.legend()

plt.tight_layout()

plt.show()