from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firestore with your credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/ALEXANDREA/WebAppX/cred.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Endpoint to retrieve transactions

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

        # Add transaction to Firestore and get the document reference
        transaction_data = {
            'Date': date,
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        }

        # Add the transaction to the 'Transactions' collection and get the document reference
        transaction_ref = db.collection('Transaction').add(transaction_data)

        return jsonify({"message": "Transaction added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
