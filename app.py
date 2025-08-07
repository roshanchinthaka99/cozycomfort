import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ✅ DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 4000)) 
    )



# ===========================
# MANUFACTURERS
# ===========================
@app.route("/manufacturers", methods=["GET"])
def get_manufacturers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM manufacturer")
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route("/manufacturer", methods=["POST"])
def add_manufacturer():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO manufacturer (model_name, material, production_capacity, stock)
        VALUES (%s, %s, %s, %s)
    """, (data["model_name"], data["material"], data["production_capacity"], data["stock"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Manufacturer added"}), 201

@app.route("/manufacturer/<string:model_name>", methods=["DELETE"])
def delete_manufacturer(model_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to delete a manufacturer by its model_name
        cursor.execute("DELETE FROM manufacturer WHERE model_name = %s", (model_name,))
        
        conn.commit()
        
        # Check if any row was deleted
        if cursor.rowcount == 0:
            return jsonify({"message": "Manufacturer not found"}), 404
        
        return jsonify({"message": "Manufacturer deleted successfully"}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error deleting manufacturer: {e}")
        return jsonify({"message": "Error processing request"}), 500
    finally:
        # Make sure the connection is closed
        if conn.is_connected():
            cursor.close()
            conn.close()


# ===========================
# DISTRIBUTORS
# ===========================
@app.route("/distributors", methods=["GET"])
def get_distributors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM distributor")
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route("/distributor", methods=["POST"])
def add_distributor():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO distributor (name, location, stock)
        VALUES (%s, %s, %s)
    """, (data["name"], data["location"], data["stock"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Distributor added"}), 201

@app.route("/distributor/<int:id>", methods=["DELETE", "OPTIONS"], strict_slashes=False)
def delete_distributor(id):
    # Handle the OPTIONS preflight request for CORS
    if request.method == 'OPTIONS':
        return jsonify(success=True), 200

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to delete a distributor by its unique ID
        cursor.execute("DELETE FROM distributor WHERE id = %s", (id,))
        
        conn.commit()
        
        # Check if a row was actually deleted
        if cursor.rowcount == 0:
            return jsonify({"message": "Distributor not found"}), 404
            
        return jsonify({"message": "Distributor deleted successfully"}), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error deleting distributor: {e}")
        return jsonify({"message": "Error processing request"}), 500
    finally:
        # Ensure the database connection is always closed
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# ===========================
# SELLERS
# ===========================
@app.route("/sellers", methods=["GET"])
def get_sellers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seller")
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route("/seller", methods=["POST"])
def add_seller():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO seller (name, store_type, stock)
        VALUES (%s, %s, %s)
    """, (data["name"], data["store_type"], data["stock"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Seller added"}), 201

@app.route("/seller/<int:id>", methods=["DELETE", "OPTIONS"], strict_slashes=False)
def delete_seller(id):
    # This handles the browser's preflight request
    if request.method == 'OPTIONS':
        return jsonify(success=True), 200

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # The SQL command to delete a seller using their unique ID
        cursor.execute("DELETE FROM seller WHERE id = %s", (id,))
        
        conn.commit()
        
        # Check if a row was deleted to confirm the seller existed
        if cursor.rowcount == 0:
            return jsonify({"message": "Seller not found"}), 404
            
        return jsonify({"message": "Seller deleted successfully"}), 200

    except Exception as e:
        # It's good practice to log errors
        print(f"Error deleting seller: {e}")
        return jsonify({"message": "Error processing request"}), 500
    finally:
        # Always close the connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ===========================
# SIMPLE ORDER PROCESS (Optional)
# ===========================
@app.route("/order", methods=["POST"])
def process_order():
    data = request.get_json()
    # Just simulate the flow, you can expand it later
    model = data.get("model_name")
    seller_id = data.get("seller_id")

    # Assume we reduce 1 stock from seller
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE seller SET stock = stock - 1 WHERE id = %s", (seller_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Order for {model} processed for seller {seller_id}"}), 200

# ===========================
# TEST ROUTE
# ===========================
@app.route("/")
def index():
    return "✅ Cozy Comfort API is working..."


