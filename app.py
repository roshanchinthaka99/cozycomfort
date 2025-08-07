!pip install flask flask-cors mysql-connector-python

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ✅ DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="3eT8otQGwJZcsNW.root",        
        password="zOV9rH1DnEIfaLI2",       
        database="test"
        port=4000,
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


