"""
All SQL queries against the retail database.
Every function uses the shared SQLAlchemy `engine` from db.py -- this is
what removes the "pandas only supports SQLAlchemy connectable" warning,
since we never pass a raw DBAPI connection to pd.read_sql().
"""

import pandas as pd
from db import engine


def get_monthly_revenue():
    q = """
        SELECT
            DATE_FORMAT(order_date, '%%Y-%%m') AS month,
            SUM(revenue) AS monthly_revenue
        FROM orders
        GROUP BY month
        ORDER BY month;
    """
    return pd.read_sql(q, engine)


def get_all_orders():
    q = "SELECT * FROM orders;"
    return pd.read_sql(q, engine)


def get_top_customers(limit=5):
    q = f"""
        SELECT
            c.customer_id,
            c.name,
            COUNT(DISTINCT o.order_id) AS num_orders,
            ROUND(AVG(o.revenue), 2) AS avg_order_value,
            ROUND(SUM(o.revenue), 2) AS lifetime_value
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY lifetime_value DESC
        LIMIT {limit};
    """
    return pd.read_sql(q, engine)


def get_top_products(limit=10):
    q = f"""
        SELECT
            product_id,
            product_name,
            SUM(quantity) AS total_quantity,
            ROUND(SUM(revenue), 2) AS revenue
        FROM orders
        GROUP BY product_id, product_name
        ORDER BY revenue DESC
        LIMIT {limit};
    """
    return pd.read_sql(q, engine)


def get_orders_by_country():
    q = """
        SELECT
            c.country,
            COUNT(DISTINCT o.order_id) AS num_orders,
            ROUND(SUM(o.revenue), 2) AS revenue
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY c.country
        ORDER BY revenue DESC;
    """
    return pd.read_sql(q, engine)


def get_daily_orders():
    q = """
        SELECT
            DATE(order_date) AS day,
            COUNT(DISTINCT order_id) AS num_orders,
            ROUND(SUM(revenue), 2) AS revenue
        FROM orders
        GROUP BY day
        ORDER BY day;
    """
    return pd.read_sql(q, engine)
