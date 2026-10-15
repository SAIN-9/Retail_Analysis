import os
import matplotlib
matplotlib.use("Agg")  # no display available inside the container
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "output"


def ensure_output_dir():
    # exist_ok=True already avoids FileExistsError for a normal directory.
    # The only way this raises is if OUTPUT_DIR path exists as a *file*.
    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        os.remove(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_monthly_revenue(monthly_df):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_df, x="month", y="monthly_revenue", marker="o")
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "monthly_revenue.png"))
    plt.close()


def plot_top_products(top_products_df):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top_products_df,
        x="revenue",
        y="product_name",
        hue="product_name",       # fixes the FutureWarning
        palette="viridis",
        legend=False,
    )
    plt.title("Top Products by Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_products.png"))
    plt.close()


def plot_top_customers(top_customers_df):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top_customers_df,
        x="lifetime_value",
        y="name",
        hue="name",
        palette="magma",
        legend=False,
    )
    plt.title("Top Customers by Lifetime Value")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_customers.png"))
    plt.close()


def plot_revenue_by_country(country_df, top_n=10):
    top = country_df.head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top,
        x="revenue",
        y="country",
        hue="country",
        palette="crest",
        legend=False,
    )
    plt.title(f"Top {top_n} Countries by Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "revenue_by_country.png"))
    plt.close()
