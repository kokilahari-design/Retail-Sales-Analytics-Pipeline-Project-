# Flask is a main class that creates your web application/ API application.
# request gives access to read incoming data from the client. Eg., read JSON body (request.get_json())
# jsonify() - Converts Python dictionaries/lists into proper JSON HTTP responses and send back to the client. JSON is the standard format for sending structured data over HTTP.
# 'send_file' reads the file and sends it to the user.(Used to serve a file from the server's file system as a response to a web request.)
# In 'send_file', as_attachment=True forces the browser to prompt a download dialog.
# render_template function uses the Jinja template engine to process the HTML file.
# pymysql - load the MySQL connector library so Python program can talk to your MySQL database.
from flask import Flask, request, jsonify, send_file, render_template
import traceback
import pymysql
from data_visualization import generate_visualization_report
import base64 # Import for encoding
import io # Import for BytesIO
import os
from datetime import datetime
# Object of Flask class is our WSGI application. Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__) 

# Database Connection
DB_CONFIG = {
    'host': "localhost",
    "user" : "root",
    "password" : "kokila",
    "database" : "retail_analytics"
}

#route() function of the Flask class is a decorator. route() decorator is used to bind URL(API endpoind) to a function(record_sale).
# GET - Retrieve or check data (optional in your API), POST - Send/submit data (your sale event) to server. Here POST method used to create a new resource
@app.route('/testing', methods = ['GET','POST']) 
def record_sale():
    connection = None  # Initialize connection to None
    cursor = None      # Initialize cursor to None
    # .get_json() method reads the JSON sent by the client and turns it into a Python dictionary.
    data = request.get_json()
    print(f"Received data: {data}")

    # 1. data validation step: checks if incoming JSON data from client contains all the necessary key fields.
    # Built-in function "all" returns True only if all keys exist in data. The "not" operator inverts the result.
    # jsonify({"msg": "error msg returned to client"}), 400 (Status code - Bad Request due to invalid or missing data)
    # cursor.lastrowid gives the auto-incremented primary key of the last row inserted through that cursor.
    if not all(k in data for k in ("customer_id", "customer_name", "product_id", "product_name", "product_category", "quantity", "price", "sale_datetime")):
        return jsonify({"message": "Missing required fields"}), 400
    
    # 2. Database Insertion
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO sales_raw (customer_id, customer_name, product_id, product_name, product_category, quantity, price, sale_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (data["customer_id"], data["customer_name"], data["product_id"],data["product_name"],data["product_category"],data["quantity"],data["price"], data["sale_datetime"])
        cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Sale recorded successfully", "order_id": cursor.lastrowid}), 201
    except Exception as e:
        print(f"Error during DB Connection: {e}")
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        print("Execution completed.")

# Defines the API endpoint as /analytics/all-reports and specifies that it only accepts HTTP GET requests (used for retrieving data).
@app.route('/analytics/all-reports', methods=['GET'])
def display_charts_in_browser():
    try:
        # 1. Generate the in-memory image data
        hourly_buffer, products_buffer = generate_visualization_report() # return two in-memory BytesIO buffers containing the PNG data, rather than saving files to disk.

        # 2. Encode image data to Base64 strings for HTML embedding 
        # Reads the binary PNG data from the hourly_buffer and converts it into a Base64 string(only way to embed binary image data directly into an HTML source code)
        # .read() gets the content; b64encode converts to bytes; .decode('utf-8') turns it into a string
        hourly_b64 = base64.b64encode(hourly_buffer.read()).decode('utf-8')
        products_b64 = base64.b64encode(products_buffer.read()).decode('utf-8')

        # 3. HTML Template for display - Here images are embedded using the data URI scheme: 'data:image/png;base64,...'

        # 4. Render and return the HTML -> render_template_string- dynamically generate the HTML content.
        return render_template(
            'charts.html',                         # Pass the name of the template html file
            hourly_b64=hourly_b64, 
            products_b64=products_b64,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        )

    except Exception as e:
        print(f"Error generating or displaying charts: {e}")
        traceback.print_exc() # Print the full stack trace to the console
        return jsonify({"message": "Error processing charts.", "error": str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True)
#run() method of Flask class runs the application on the local development server.
