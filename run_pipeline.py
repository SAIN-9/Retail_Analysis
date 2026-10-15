import time
import numpy as np
from sqlalchemy import text

from db import engine
from load_real_data import load_real_data
import queries
import visualize


def wait_for_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:
            print(f"Waiting for MySQL... ({attempt + 1}/{retries}) {e}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to MySQL after several retries.")


def clear_old_data():
    print("Clearing old data (if any)...")
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS orders"))
        conn.execute(text("DROP TABLE IF EXISTS products"))
        conn.execute(text("DROP TABLE IF EXISTS customers"))


def load_into_mysql(customers, products, orders):
    print("Loading data into MySQL...")
    customers.to_sql("customers", engine, if_exists="replace", index=False)
    products.to_sql("products", engine, if_exists="replace", index=False)
    orders.to_sql("orders", engine, if_exists="replace", index=False)


def run_numpy_analysis(monthly_df, orders_df):
    print("Running numpy analysis...")
    revenue = monthly_df["monthly_revenue"].to_numpy(dtype=float)

    stats = {
        "mean_monthly_revenue": float(np.mean(revenue)),
        "std_monthly_revenue": float(np.std(revenue)),
        "min_month_revenue": float(np.min(revenue)),
        "max_month_revenue": float(np.max(revenue)),
    }
    if len(revenue) > 1 and revenue[0] != 0:
        stats["month_over_month_growth_pct"] = float(
            (revenue[-1] - revenue[0]) / revenue[0] * 100
        )
    print(f"Revenue trend stats: {stats}")

    # Simple outlier detection on order revenue using the IQR method
    order_rev = orders_df["revenue"].to_numpy(dtype=float)
    q1, q3 = np.percentile(order_rev, [25, 75])
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    outliers = orders_df[orders_df["revenue"] > upper_bound]
    print(f"Outlier orders found: {len(outliers)}")

    return stats, outliers


def main():
    print("Starting retail analytics pipeline...")

    print("Connecting to MySQL...")
    wait_for_db()

    print("Loading real dataset (UCI Online Retail)...")
    customers, products, orders = load_real_data("data/online_retail.csv")

    clear_old_data()
    load_into_mysql(customers, products, orders)

    print("Running SQL queries...")
    monthly_df = queries.get_monthly_revenue()
    orders_df = queries.get_all_orders()
    top_customers_df = queries.get_top_customers(limit=5)
    top_products_df = queries.get_top_products(limit=10)
    country_df = queries.get_orders_by_country()

    run_numpy_analysis(monthly_df, orders_df)

    print("Top 5 customers by lifetime value:")
    print(top_customers_df)

    print("Generating charts...")
    visualize.ensure_output_dir()
    visualize.plot_monthly_revenue(monthly_df)
    visualize.plot_top_products(top_products_df)
    visualize.plot_top_customers(top_customers_df)
    visualize.plot_revenue_by_country(country_df)

    print("\nPipeline complete. Charts saved to the output/ folder.")


if __name__ == "__main__":
    main()
