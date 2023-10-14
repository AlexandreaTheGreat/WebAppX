from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8080"}})

# Initialize Firestore with your credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/ALEXANDREA/WebAppX/cred.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Endpoint to retrieve transactions
@app.route('/api/Transactions', methods=['GET'])
def get_all_transactions():
    try:
        # Retrieve transactions from Firestore
        transactions = []
        transaction_docs = db.collection('Transactions').stream()

        for doc in transaction_docs:
            transaction = doc.to_dict()
            transaction['id'] = doc.id  # Include the transaction ID in the response
            transactions.append(transaction)

        return jsonify({"transactions": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/Transactions', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        date = data.get('Date')
        product_name = data.get('Name')
        amount = data.get('Amount')
        price = data.get('Price')
        transaction_type = data.get('Type')

        # Validate input data here if necessary

        # Add transaction to Firestore based on Type
        transaction_data = {
            'Date': date,
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        }
        
        transaction_data2 = {
            'Date': date,
            'Name': product_name,
            'Amount': amount,
            'Price': price
        }
        transaction_ref = db.collection('Transactions').add(transaction_data)

        # Check Type and store transaction in appropriate collection
        if transaction_type == 1:
            db.collection('Expenses').add(transaction_data2)
        elif transaction_type == 2:
            db.collection('Sales').add(transaction_data2)
        else:
            return jsonify({"error": "Invalid transaction type"}), 400

        return jsonify({"message": "Transaction added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@app.route('/api/Transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Delete transaction from Firestore using transaction_id
        transaction_ref = db.collection('Transactions').document(transaction_id)
        transaction_ref.delete()

        return jsonify({"message": "Transaction deleted successfully "+transaction_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/Transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        data = request.get_json()
        transaction_date = data.get('Date')
        product_name = data.get('Name')
        amount = data.get('Amount')
        price = data.get('Price')
        transaction_type = data.get('Type')

        # Validate input data here if necessary

        # Update transaction in Firestore using transaction_id
        transaction_date = datetime.strptime(transaction_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        transaction_ref = db.collection('Transactions').document(transaction_id)
        transaction_ref.set({
            'Date': transaction_date,
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        })

        return jsonify({"message": "Transaction updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
