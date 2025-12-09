import random
from datetime import datetime

CUSTOMER_NAMES = ["kokila", "Sandy", "Kalai", "Hari", "Viswa", "Sharvesh", "Vedanth", "Hema", "Deebika", "David", "Henry",
    "John", "Jack", "Kavya", "Raja", "Mia", "Ravi", "Oviya", "Pranav",
    "Jerry", "Riya", "Sophia", "Tom"]

# Create ID → Name mapping  #enumerate function here results - {loc + 1: name}
CUSTOMER_MAP = {i+1: name for i, name in enumerate(CUSTOMER_NAMES)}

PRODUCTS = {
    1001: ("Mobile Phone", "Electronics"),
    1002: ("Laptop", "Electronics"),
    1003: ("Wireless Mouse", "Accessories"),
    1004: ("Bluetooth Speaker", "Electronics"),
    1005: ("Headphones", "Accessories"),
    1006: ("Air Conditioner", "Home Appliance"),
    1007: ("Refrigerator", "Home Appliance"),
    1008: ("Coffee Maker", "Kitchen Appliance"),
    1009: ("Smart Watch", "Electronics"),
    1010: ("Gaming Console", "Entertainment"),
    1011: ("Jeans", "Dress"),
    1015: ("Shirt", "Dress")
}

def generate_sale_event():

    # Simulates one transaction

    customerid = random.choice(list(CUSTOMER_MAP.keys()))   # Get all customer IDs from CUSTOMER_MAP.keys(), Randomly pick ONE ID
    customer_name = CUSTOMER_MAP[customerid] #Look up the selected customerid in the dictionary and Retrieve the matching customer_name
    productid = random.choice(list(PRODUCTS.keys()))  # Get all Product IDs from PRODUCTS.keys(), Randomly pick ONE ID
    product_name, product_category = PRODUCTS[productid] #Look up the selected productid in the dictionary and Retrieve the matching product_name and product_category
    quantity = random.randint(1, 5) # Pick a random number between 1 and 5
    price = round(random.uniform(10.0, 1000.0), 2) # Round the randomly generated decimal number between 10.00 and 1000.00 with 2 decimal places
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Get current date and time, convert into string format("2025-12-06 17:18:25")
    
    return {
        "customer_id": customerid,
        "customer_name": customer_name,
        "product_id": productid,
        "product_name": product_name,
        "product_category": product_category,
        "quantity": quantity,
        "price": price,
        "sale_datetime": timestamp
    }

# Run this script periodically to send data (via API)
print(generate_sale_event())
