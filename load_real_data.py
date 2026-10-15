"""
Loads the real UCI "Online Retail" dataset (data/online_retail.csv) and
reshapes it into three tables that mirror the schema the rest of the
pipeline (queries.py) already expects: customers, products, orders.

Download the CSV from:
  https://www.kaggle.com/datasets/vijayuv/onlineretail
  (or https://archive.ics.uci.edu/dataset/352/online+retail)
and place it at: data/online_retail.csv
"""

import pandas as pd

def load_and_clean(csv_path="data/online_retail.csv"):
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    df = df.rename(columns={
        "InvoiceNo": "order_id",
        "StockCode": "product_id",
        "Description": "product_name",
        "Quantity": "quantity",
        "InvoiceDate": "order_date",
        "UnitPrice": "unit_price",
        "CustomerID": "customer_id",
        "Country": "country",
    })
    # Drop rows with no customer attached -- can't attribute the order
    df = df.dropna(subset=["customer_id"])

    # Drop cancelled orders (InvoiceNo starting with 'C')
    df = df[~df["order_id"].astype(str).str.startswith("C")]

    # Drop bad rows (returns / data entry errors show up as <= 0)
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    # Drop rows with no product description
    df = df.dropna(subset=["product_name"])

    df["customer_id"] = df["customer_id"].astype(int)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)

    return df


def build_tables(df):
    """Split the flat, cleaned DataFrame into normalized tables."""

    # --- customers ---
    # The raw dataset has no customer name, only an ID + country, so we
    # synthesize a display name. Replace this if you have a real name source.
    customers = (
        df[["customer_id", "country"]]
        .drop_duplicates(subset=["customer_id"])
        .copy()
    )
    customers["name"] = "Customer " + customers["customer_id"].astype(str)
    customers = customers[["customer_id", "name", "country"]]

    # --- products ---
    products = (
        df[["product_id", "product_name"]]
        .drop_duplicates(subset=["product_id"])
        .copy()
    )

    # --- orders ---
    orders = df[[
        "order_id", "customer_id", "product_id", "product_name",
        "quantity", "unit_price", "revenue", "order_date",
    ]].copy()

    return customers, products, orders


def load_real_data(csv_path="data/online_retail.csv"):
    df = load_and_clean(csv_path)
    customers, products, orders = build_tables(df)
    return customers, products, orders
