CREATE DATABASE IF NOT EXISTS retail_analytics;
use retail_analytics;
create table if not exists sales_raw (
order_id int auto_increment primary key,
customer_id int not null,
customer_name varchar(100) not null,
product_id int not null,
product_name varchar(100) not null,
product_category varchar(100) not null,
quantity int not null,
price decimal(10,2) not null,
sale_datetime timestamp default current_timestamp
);
# Total revenue with multiple products allowed per hour
create table if not exists hourly_sales_summary (
aggregation_hour DATETIME NOT NULL,
product_name VARCHAR(100) NOT NULL,
product_category VARCHAR(100) NOT NULL,
total_quantity INT NOT NULL,
total_revenue DECIMAL(10, 2) NOT NULL,
PRIMARY KEY(aggregation_hour, product_name, product_category)
);
