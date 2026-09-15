import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("python_app")

from db_connection import create_connection


# Connect to MySQL
connection = create_connection()

query = """
    SELECT
        month,
        revenue
    FROM monthly_revenue
    ORDER BY month
"""

df = pd.read_sql(query, connection)

connection.close()


# Display data
print(df)


# Create chart
plt.figure(figsize=(10, 5))

plt.plot(
    df["month"],
    df["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()