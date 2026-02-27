# DAG class (Directed Acyclic Graph) creates a new DAG. It defines What tasks exist, In what order they should run, When they should run (schedule), How they behave (retries, timeout, owner, etc.)
# PythonOperator class runs any Python function as airflow task inside a DAG. Airflow tasks must be wrapped inside operators
from Analysis_app import DB_CONFIG
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymysql

def transform_and_load_data(**kwargs): # (**kwargs) → Airflow passes context variables (like execution_date, task_instance, etc.), else don't pass args.
    # This task connects to the DB, reads all raw data, aggregates with Pandas, and writes to summary table.
    # You should also use connection.autocommit(False) explicitly for transaction control.
    try:        
        connection = pymysql.connect(**DB_CONFIG)

        # 1. Extraction (E) - Read all raw data   # Instead of selecting all data every time, filter: WHERE sale_datetime >= execution_date to avoid reprocessing everything.
        df = pd.read_sql("SELECT * FROM sales_raw", connection)
        print(f" Extraction data from mysql:{df}")

         # 2. Transformation (T) - Pandas Grouping
         #.dt - Datetime accessor to access specialized time-series properties and methods (like .hour, .day, .floor(), etc.)
         # .floor('H') - moves the timestamp to the start of the hour. All mins, secs, and microseconds are reset to zero. (Eg., 2025-12-06 14:37:55 becomes 2025-12-06 14:00:00)
        df["Revenue"] = df["quantity"] * df["price"]
        print(f"revenue is :", df["Revenue"])
        df['hour'] = df['sale_datetime'].dt.floor('h') # Grouping sales hour by hour.x
        summary_df = df.groupby(['hour','product_name', 'product_category']).agg(   # Groups data by hour, product_name
            total_quantity=('quantity', 'sum'),      # Calculates total revenue , total quantity sold in that hour
            total_revenue = ("Revenue","sum")).reset_index()  # .reset_index() converts groupby result back into a regular DataFrame.
        print(f"After transformation of data: {summary_df}") 

         # 3. Load (L) - Write to summary table
         # ON DUPLICATE KEY UPDATE - If row already exists, MySQL should NOT fail - instead, it should update that existing row.
        cursor = connection.cursor() 
        for index,row in summary_df.iterrows(): # Iterates through each row of the summary DataFrame # For very large datasets, .iterrows() is slow. Bulk inserts - executemany() would be better.
            insert_query = """
            Insert into hourly_sales_summary(aggregation_hour, product_name, product_category, total_quantity, total_revenue)
            Values (%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            total_quantity=VALUES(total_quantity),
            total_revenue=VALUES(total_revenue);
            """
            cursor.execute(insert_query, (row['hour'], row['product_name'], row['product_category'], row['total_quantity'], row['total_revenue']))
        connection.commit()

        cursor.execute("SELECT * FROM hourly_sales_summary;")
        print("\nCurrent Summary Table:")
        for result in cursor.fetchall():
            print(result)

        connection.close()
        print(f"Successfully loaded {len(summary_df)} summary records.")
    except Exception as e:
        print(f"ETL Error: {e}")

with DAG(                      # Create a new workflow and attach tasks inside it
    dag_id='retail_sales_etl', # Unique name of your workflow
   schedule_interval=timedelta(hours=1), # Run the workflow every 1 hour
    catchup=False # Do NOT run missing historical runs
) as dag:
    
    transform_task = PythonOperator(     #Create a task that runs a Python function
        task_id='Transform_load_Sales_Data',  # Name of the task
        python_callable=transform_and_load_data, # Function executed when the task runs
    )

