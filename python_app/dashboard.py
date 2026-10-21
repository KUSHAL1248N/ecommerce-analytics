
import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import create_connection

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Analytics Dashboard")
st.caption("Sales, customer, product, and order insights")


# ---------------------------------
# DATABASE QUERY FUNCTION
# ---------------------------------
@st.cache_data(ttl=60)
def load_query(query, params=None):
    connection = create_connection()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


# ---------------------------------
# LOAD FILTER OPTIONS
# ---------------------------------
@st.cache_data(ttl=60)
def load_filter_options():
    dates = load_query("""
        SELECT
            MIN(DATE(order_date)) AS min_date,
            MAX(DATE(order_date)) AS max_date
        FROM orders
    """)

    statuses = load_query("""
        SELECT DISTINCT status
        FROM orders
        WHERE status IS NOT NULL
        ORDER BY status
    """)

    return dates, statuses


# ---------------------------------
# LOAD FILTERED DASHBOARD DATA
# ---------------------------------
@st.cache_data(ttl=60)
def load_data(start_date, end_date, selected_status):

    date_params = (start_date, end_date)

    status_filter = ""
    status_params = ()

    if selected_status != "All":
        status_filter = " AND status = %s"
        status_params = (selected_status,)

    # Business overview
    overview = load_query("""
        SELECT
            (SELECT COUNT(*) FROM customers) AS customers,
            (SELECT COUNT(*) FROM products) AS products,
            COUNT(*) AS orders,

            COALESCE(SUM(
                CASE WHEN status = 'Delivered'
                THEN 1 ELSE 0 END
            ), 0) AS delivered_orders,

            COALESCE(SUM(
                CASE WHEN status = 'Delivered'
                THEN total_amount ELSE 0 END
            ), 0) AS revenue,

            COALESCE(AVG(
                CASE WHEN status = 'Delivered'
                THEN total_amount END
            ), 0) AS avg_order_value

        FROM orders
        WHERE DATE(order_date) BETWEEN %s AND %s
    """ + status_filter, date_params + status_params)

    # Monthly revenue
    monthly = load_query("""
        SELECT
            DATE_FORMAT(order_date, '%Y-%m') AS month,
            COUNT(*) AS total_orders,

            COALESCE(SUM(
                CASE WHEN status = 'Delivered'
                THEN total_amount ELSE 0 END
            ), 0) AS revenue

        FROM orders
        WHERE DATE(order_date) BETWEEN %s AND %s
    """ + status_filter + """
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY month
    """, date_params + status_params)

    # Category revenue: delivered orders only
    category_status_clause = "AND o.status = 'Delivered'"

    if selected_status not in ("All", "Delivered"):
        category_status_clause = "AND 1 = 0"

    categories = load_query("""
        SELECT
            c.category_name AS category,
            SUM(oi.quantity * oi.unit_price) AS revenue

        FROM categories c
        JOIN products p
            ON c.category_id = p.category_id
        JOIN order_items oi
            ON p.product_id = oi.product_id
        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE DATE(o.order_date) BETWEEN %s AND %s
    """ + category_status_clause + """
        GROUP BY c.category_id, c.category_name
        ORDER BY revenue DESC
    """, date_params)

    # Top products by delivered item revenue
    product_status_clause = "AND o.status = 'Delivered'"

    if selected_status not in ("All", "Delivered"):
        product_status_clause = "AND 1 = 0"

    products = load_query("""
        SELECT
            p.product_name,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.quantity * oi.unit_price) AS revenue,
            MAX(pp.profit) AS profit

        FROM products p
        JOIN order_items oi
            ON p.product_id = oi.product_id
        JOIN orders o
            ON oi.order_id = o.order_id

        LEFT JOIN (
            SELECT
                product_name,
                MAX(profit) AS profit
            FROM product_performance
            GROUP BY product_name
        ) pp
            ON pp.product_name = p.product_name

        WHERE DATE(o.order_date) BETWEEN %s AND %s
    """ + product_status_clause + """
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 10
    """, date_params)

    # Order status distribution for selected dates
    statuses = load_query("""
        SELECT
            status,
            COUNT(*) AS orders
        FROM orders
        WHERE DATE(order_date) BETWEEN %s AND %s
        GROUP BY status
        ORDER BY orders DESC
    """, date_params)

    return overview, monthly, categories, products, statuses


# ---------------------------------
# CUSTOMER LIFETIME VALUE
# ---------------------------------
@st.cache_data(ttl=60)
def load_top_customers():
    return load_query("""
        SELECT
            customer_name,
            total_orders,
            lifetime_value
        FROM customer_lifetime_value
        ORDER BY lifetime_value DESC
        LIMIT 10
    """)


# ---------------------------------
# MAIN DASHBOARD
# ---------------------------------
try:
    dates, status_data = load_filter_options()

    if dates.empty or pd.isna(dates.iloc[0]["min_date"]):
        st.warning("No order dates are available in the database.")
        st.stop()

    min_date = pd.to_datetime(
        dates.iloc[0]["min_date"]
    ).date()

    max_date = pd.to_datetime(
        dates.iloc[0]["max_date"]
    ).date()

    available_statuses = (
        status_data["status"].dropna().tolist()
    )

    # Filters
    st.subheader("Filters")

    f1, f2, f3 = st.columns([2, 2, 1])

    with f1:
        start_date = st.date_input(
            "Start date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with f2:
        end_date = st.date_input(
            "End date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    with f3:
        selected_status = st.selectbox(
            "Order status",
            ["All"] + available_statuses
        )

    if start_date > end_date:
        st.error(
            "Start date must be on or before the end date."
        )
        st.stop()

    # Fetch data for selected filters
    overview, monthly, categories, products, statuses = load_data(
        start_date.isoformat(),
        end_date.isoformat(),
        selected_status
    )

    if overview.empty:
        st.warning("No overview data is available.")
        st.stop()

    metrics = overview.iloc[0]

    st.caption(
        f"Showing orders from {start_date} to {end_date} "
        f"| Status: {selected_status}"
    )

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Customers (all)",
        f"{int(metrics['customers']):,}"
    )

    col2.metric(
        "Products (all)",
        f"{int(metrics['products']):,}"
    )

    col3.metric(
        "Orders in Filter",
        f"{int(metrics['orders']):,}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Delivered Orders in Filter",
        f"{int(metrics['delivered_orders']):,}"
    )

    col5.metric(
        "Delivered Revenue in Filter",
        f"₹{float(metrics['revenue']):,.2f}"
    )

    col6.metric(
        "Average Delivered Order",
        f"₹{float(metrics['avg_order_value']):,.2f}"
    )

    st.divider()

    # Monthly revenue chart
    st.subheader("Monthly Revenue")

    if not monthly.empty:
        monthly["revenue"] = pd.to_numeric(
            monthly["revenue"], errors="coerce"
        ).fillna(0)

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Delivered Revenue by Month"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.info("No monthly data for these filters.")

    # Category and order-status charts
    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Category")

        if not categories.empty:
            fig = px.bar(
                categories,
                x="category",
                y="revenue",
                title="Delivered Item Revenue by Category"
            )

            fig.update_layout(
                xaxis_title="Category",
                yaxis_title="Revenue (₹)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            st.info(
                "No delivered category revenue for these filters."
            )

    with right:
        st.subheader("Order Status")

        if not statuses.empty:
            fig = px.pie(
                statuses,
                names="status",
                values="orders",
                hole=0.45,
                title="Orders by Status in Selected Dates"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            st.info("No order statuses for these dates.")

    # Top products
    st.divider()
    st.subheader("Top 10 Products by Delivered Item Revenue")

    if not products.empty:
        products["revenue"] = pd.to_numeric(
            products["revenue"], errors="coerce"
        ).fillna(0)

        products["units_sold"] = pd.to_numeric(
            products["units_sold"], errors="coerce"
        ).fillna(0)

        fig = px.bar(
            products.sort_values(
                "revenue", ascending=True
            ),
            x="revenue",
            y="product_name",
            orientation="h",
            title="Top Products",
            hover_data=["units_sold", "profit"]
        )

        fig.update_layout(
            xaxis_title="Item Revenue (₹)",
            yaxis_title="Product",
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            products,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Product Report (CSV)",
            data=products.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="top_products.csv",
            mime="text/csv"
        )
    else:
        st.info("No delivered product sales for these filters.")

    # Customer lifetime value analysis
    st.divider()
    st.subheader("🏆 Top 10 Customers by Lifetime Value")

    st.caption(
        "All-time customer spending from the "
        "customer_lifetime_value SQL view."
    )

    customers = load_top_customers()

    if not customers.empty:
        customers["lifetime_value"] = pd.to_numeric(
            customers["lifetime_value"],
            errors="coerce"
        ).fillna(0)

        customers["total_orders"] = pd.to_numeric(
            customers["total_orders"],
            errors="coerce"
        ).fillna(0)

        left, right = st.columns([3, 2])

        with left:
            customer_chart = px.bar(
                customers.sort_values(
                    "lifetime_value", ascending=True
                ),
                x="lifetime_value",
                y="customer_name",
                orientation="h",
                title="Highest-Value Customers",
                hover_data=["total_orders"]
            )

            customer_chart.update_layout(
                xaxis_title="Lifetime Value (₹)",
                yaxis_title="Customer",
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(
                customer_chart,
                use_container_width=True
            )

        with right:
            st.dataframe(
                customers,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "Download Customer Report (CSV)",
            data=customers.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="top_customers.csv",
            mime="text/csv"
        )
    else:
        st.info(
            "No customer lifetime value data is available."
        )

    st.caption("Dashboard data is cached for up to 60 seconds.")

except Exception as error:
    st.error(
        "The dashboard could not load data from MySQL."
    )

    st.info(
        "Check that MySQL is running, the .env settings are correct, "
        "and the required tables and views exist."
    )

    with st.expander("Technical error details"):
        st.code(str(error))
