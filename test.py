# requests is to send HTTP requests (like GET, POST, PUT, DELETE) and work with APIs easily.
# time module is to handle time-related tasks like delays, timestamps, and measuring intervals.
import requests
import time
import random
from data_generator import generate_sale_event

API_URL = "http://127.0.0.1:5000/testing"

# Run this loop while Flask server is running
# Using a counter to break the loop for demonstration purposes.
MAX_SALES = 5
sale_count = 0

print(f"--- Sales Event Processor Started (Max {MAX_SALES} Events) ---")
print("Enter 'exit' or 'q' at the prompt to terminate the program early.")
print("-" * 40)

while True:
    # 1. Check for termination command or MAX_SALES limit
    if sale_count >= MAX_SALES:
        print(f"\nMAX_SALES limit ({MAX_SALES}) reached. Terminating loop.")
        break
    
    user_input = input("Press ENTER to generate and send a sale event, or type 'exit' or 'q': ").strip().lower()

    if user_input in ['exit', 'q']:
        print("\nTermination signal received. Exiting program.")
        break

    # 2. Process Sale Event
    
    sale_data = generate_sale_event()
    print(f"\nFetching sales data entry: {sale_data}")
    
    try:
        # sends an HTTP POST request to the API endpoint server with the generated sale data as JSON payload
        response = requests.post(API_URL, json=sale_data)
        print(f"Response from server: {response}")
        
        if response.status_code == 201:
            print(f"SUCCESS: Event ID {response.json().get('id', 'N/A')}")  # response.json() → parses the JSON response from the server into a Python dictionary.
            # Increment the counter only upon successful submission
            sale_count += 1
            print(f"Current Sale Count: {sale_count} / {MAX_SALES}")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"API server is not running or connection failed: {e}")
        # Terminate if the server is unreachable
        break

    time.sleep(random.uniform(1, 3))  # Wait 1-3 seconds for next "real-time" event


