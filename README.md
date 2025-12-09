# Retail-Sales-Analytics-Pipeline-Project-
Architecture: [Flask API] → [MySQL Staging] → [Airflow ETL] → [MySQL Reporting] → [Flask Dashboard]
Built a real-time retail analytics system using a Flask REST API to ingest JSON-based sales transactions and store them in a MySQL staging table via Pymysql. Developed a Python script to simulate randomized retail sales events enabling continuous pipeline ingestion.
Implemented a scheduled ETL workflow using Apache Airflow, connecting to MySQL to extract raw staging data, transform & aggregate it using Pandas, and load analytics-ready datasets into reporting tables. Automated hourly ETL workflows to ensure that reporting tables always contain the latest cleaned, aggregated, and validated insights.
Created dynamic data visualizations using Matplotlib, embedded directly into a Flask-based HTML dashboard for on-demand reporting. 

