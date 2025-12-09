#from Analysis_app import DB_CONFIG
import pymysql
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import io

# Database Connection
DB_CONFIG = {
    'host': "localhost",
    "user" : "root",
    "password" : "kokila",
    "database" : "retail_analytics"
}

def generate_visualization_report():

    # 1. Extraction (Get last 24 hours of data)
    connection = pymysql.connect(**DB_CONFIG)
    time_24h_ago = datetime.now() - timedelta(hours=24)
    time_24h_ago_ftime = time_24h_ago.replace(minute=0, second=0, microsecond=0)   
    print(f"time_24h_ago is {time_24h_ago}")
    print(f"time_24h_ago_ftime is {time_24h_ago_ftime.strftime('%Y-%m-%d %H:%M:%S')}")
    query = """
    SELECT * FROM hourly_sales_summary 
    WHERE aggregation_hour >= %s
    ORDER BY aggregation_hour DESC;
    """
    df = pd.read_sql(query, connection, params=(time_24h_ago_ftime,))
    # The variable must be wrapped in a tuple or list inside params, even if it's a single item.
    print(df)
    connection.close()

    # If no data, exit
    if df.empty:
        print("No recent data for analysis.")
        return
    
    # --- 2. Visualization (Matplotlib) ---
    
    # A. Total Revenue Trend - Calculates the total revenue for each unique hour in the dataset.
    # Groups by aggregation_hour column, calculates the sum of the total_revenue for each hour, and converts the result back into a standard DataFrame with indexed columns.
    hourly_revenue = df.groupby('aggregation_hour')['total_revenue'].sum().reset_index()
    print("hourly_revenue:",hourly_revenue)
    
    plt.figure(figsize=(12, 6)) # 12 inches wide by 6 inches tall.
    plt.plot(hourly_revenue['aggregation_hour'], hourly_revenue['total_revenue'], marker='o')  # Line Chart
    plt.title('Last 24 Hours Total Revenue Trend')
    plt.xlabel('Hour of Day')
    plt.ylabel('Total Revenue')
    plt.grid(True)
    plt.xticks(rotation=45) # Rotates the labels on the x-axis.
    plt.tight_layout() # Automatically adjusts plot parameters.
    # Use os.path.join for clean, cross-platform path to the target directory
    # Save to in-memory buffer instead of disk file
    hourly_buffer = io.BytesIO()
    plt.savefig(hourly_buffer, format='png')
    #plt.savefig(os.path.join(CHECK_DIR, 'analytics_hourly_trend.png')) # Saves the generated plot to a file.
    plt.close()

    # B. Top 5 Products by Revenue
    # Groups by product_name, sums the total_revenue for each product, sorts the results in descending order (highest revenue first), and selects only the top 5 products.
    product_revenue = df.groupby('product_name')['total_revenue'].sum().sort_values(ascending=False).head(5) # Data Aggregation & Filtering
    print(product_revenue)
    
    plt.figure(figsize=(8, 5))
    product_revenue.plot(kind='bar') # Generates a bar plot  directly from the Pandas Series product_revenue
    plt.title('Top 5 Products by Revenue (Last 24H)')
    plt.xlabel('Product Name')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=0)
    plt.tight_layout()
    products_buffer = io.BytesIO()
    plt.savefig(products_buffer, format='png')
    #plt.savefig(os.path.join(CHECK_DIR, 'analytics_top_products.png'))
    plt.close()

    # Reset buffer pointers and return the two buffers
    hourly_buffer.seek(0)
    products_buffer.seek(0)

    return hourly_buffer, products_buffer

if __name__ == "__main__":
    generate_visualization_report()
