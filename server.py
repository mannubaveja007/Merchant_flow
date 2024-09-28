from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import jwt
import datetime
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/merchant_dashboard"
mongo = PyMongo(app)



SECRET_KEY = "BSxdVauBG5aucIigt-sz6WTCTHjDrxHtl7CdVaBIiYjo_LULd3BPLcksS-kGSuLo"  


PAYME_CLIENT_ID = "2yXv7N4kGwQToO7McZZz1kG9QarBDbyR"
PAYME_CLIENT_SECRET = "BSxdVauBG5aucIigt-sz6WTCTHjDrxHtl7CdVaBIiYjo_LULd3BPLcksS-kGSuLo"

@app.route("/")
def home():
    return "Welcome to the Merchant Dashboard!"

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token.split()[1], SECRET_KEY, algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({"message": "User not found!"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(current_user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/auth/register', methods=['POST'])
def register():
    auth_data = request.json
    if mongo.db.users.find_one({"username": auth_data['username']}):
        return jsonify({"message": "User already exists!"}), 400
    
    user_data = {
        "username": auth_data['username'],
        "password": auth_data['password'],  
        "created_at": datetime.datetime.utcnow()
    }
    
    user_id = mongo.db.users.insert_one(user_data).inserted_id
    return jsonify({"user_id": str(user_id), "message": "User registered successfully!"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    auth_data = request.json
    user = mongo.db.users.find_one({"username": auth_data['username'], "password": auth_data['password']})
    if user:
        token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials!"}), 401





@app.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    product_data = request.json
    product_data['merchant_id'] = str(current_user['_id'])  # Associate product with the user
    product_id = mongo.db.products.insert_one(product_data).inserted_id
    return jsonify({"product_id": str(product_id), "message": "Product created successfully!"}), 201

@app.route('/products/<product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    product = mongo.db.products.find_one({
        "_id": ObjectId(product_id),
        "merchant_id": str(current_user['_id'])  # Ensure the product belongs to the current user
    })
    
    if product:
        # Convert ObjectId and any other non-serializable types to strings
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
        return jsonify(product), 200
    
    return jsonify({"message": "Product not found!"}), 404
@app.route('/products/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    product_data = request.json
    result = mongo.db.products.update_one(
        {"_id": ObjectId(product_id), "merchant_id": str(current_user['_id'])},
        {"$set": product_data}
    )
    
    if result.modified_count > 0:
        return jsonify({"message": "Product updated successfully!"}), 200
    return jsonify({"message": "Product not found or no changes made!"}), 404

@app.route('/products/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    result = mongo.db.products.delete_one(
        {"_id": ObjectId(product_id), "merchant_id": str(current_user['_id'])}
    )
    
    if result.deleted_count > 0:
        return jsonify({"message": "Product deleted successfully!"}), 200
    return jsonify({"message": "Product not found!"}), 404

@app.route('/payments/transfer', methods=['POST'])
@token_required
def transfer_money(current_user):
    transfer_data = request.json
    response = requests.post("https://api.payme.com/transfer", json={
        "client_id": PAYME_CLIENT_ID,
        "client_secret": PAYME_CLIENT_SECRET,
        "amount": transfer_data['amount'],
        "to_account": transfer_data['to_account']
    })
    
    if response.status_code == 200:
        return jsonify({"message": "Transfer successful!", "data": response.json()}), 200
    else:
        return jsonify({"message": "Transfer failed!", "error": response.json()}), response.status_code

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello {current_user['username']}! This is a protected route."})


# Invoice Management CRUD Operations

@app.route('/invoices', methods=['POST'])
@token_required
def create_invoice(current_user):
    invoice_data = request.json
    invoice_data['merchant_id'] = str(current_user['_id'])  # Associate invoice with the user
    invoice_data['status'] = 'pending'  # Default status for new invoices
    
    invoice_id = mongo.db.invoices.insert_one(invoice_data).inserted_id
    return jsonify({"invoice_id": str(invoice_id), "message": "Invoice created successfully!"}), 201

@app.route('/invoices/<invoice_id>', methods=['GET'])
@token_required
def get_invoice(current_user, invoice_id):
    invoice = mongo.db.invoices.find_one({
        "_id": ObjectId(invoice_id),
        "merchant_id": str(current_user['_id'])  # Ensure the invoice belongs to the current user
    })
    
    if invoice:
        invoice['_id'] = str(invoice['_id'])  # Convert ObjectId to string
        return jsonify(invoice), 200
    
    return jsonify({"message": "Invoice not found!"}), 404

@app.route('/invoices/<invoice_id>', methods=['PUT'])
@token_required
def update_invoice(current_user, invoice_id):
    invoice_data = request.json
    result = mongo.db.invoices.update_one(
        {"_id": ObjectId(invoice_id), "merchant_id": str(current_user['_id'])},
        {"$set": invoice_data}
    )
    
    if result.modified_count > 0:
        return jsonify({"message": "Invoice updated successfully!"}), 200
    return jsonify({"message": "Invoice not found or no changes made!"}), 404

@app.route('/invoices/<invoice_id>', methods=['DELETE'])
@token_required
def delete_invoice(current_user, invoice_id):
    result = mongo.db.invoices.delete_one(
        {"_id": ObjectId(invoice_id), "merchant_id": str(current_user['_id'])}
    )
    
    if result.deleted_count > 0:
        return jsonify({"message": "Invoice deleted successfully!"}), 200
    return jsonify({"message": "Invoice not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True)