from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid

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
        product_name = data.get('Name')
        amount = data.get('Amount')
        price = data.get('Price')
        transaction_type = data.get('Type')

        # Validate input data here if necessary
        transaction_type = int(transaction_type)

        # Get current system time
        current_time = datetime.now()
        ID = str(uuid.uuid4())

        # Add transaction to Firestore based on Type with current system time
        transaction_data = {
            'ID': ID,
            'Date': datetime.utcfromtimestamp(current_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S'),  # Store timestamp in Firestore
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        }
        
        transaction_data2 = {
            'ID': ID,
            'Date': datetime.utcfromtimestamp(current_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S'),
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
        transaction_ID = data.get('ID')
        transaction_date = data.get('Date')
        product_name = data.get('Name')
        amount = data.get('Amount')
        price = data.get('Price')
        transaction_type = data.get('Type')

        # Validate input data here if necessary

        # Retrieve the original transaction data
        original_transaction = db.collection('Transactions').document(transaction_id).get().to_dict()
        original_transaction_type = str(original_transaction.get('Type'))
        
        current_time = datetime.now()
        # Update transaction in Firestore using transaction_id
        transaction_date = datetime.utcfromtimestamp(current_time.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        transaction_ref = db.collection('Transactions').document(transaction_id)
        transaction_ref.set({
            'ID': transaction_ID,
            'Date': transaction_date,
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        })
        
        # Check if transaction type is changed
        if original_transaction_type != transaction_type:
            # Delete the original transaction from the appropriate collection
            if original_transaction_type == '1':
                print("Item {} deleted from expenses".format(transaction_ID))
                expense_doc = db.collection('Expenses').where('ID', '==', transaction_ID).stream()
                for doc in expense_doc:
                    doc.reference.delete()
            elif original_transaction_type == '2':
                print("Item {} deleted from sales".format(transaction_ID))
                sales_doc = db.collection('Sales').where('ID', '==', transaction_ID).stream()
                for doc in sales_doc:
                    doc.reference.delete()

            # Add the updated transaction to the new collection
            if transaction_type == '1':
                db.collection('Expenses').document(transaction_ID).set({
                    'ID': transaction_ID,
                    'Date': transaction_date,
                    'Name': product_name,
                    'Amount': amount,
                    'Price': price
                })
            elif transaction_type == '2':
                db.collection('Sales').document(transaction_ID).set({
                    'ID': transaction_ID,
                    'Date': transaction_date,
                    'Name': product_name,
                    'Amount': amount,
                    'Price': price
                })

        return jsonify({"message": "Transaction updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/Scheduled', methods=['GET'])
def get_sched_transactions():
    try:
        # Retrieve transactions from Firestore
        transactions = []
        transaction_docs = db.collection('Scheduled').stream()

        for doc in transaction_docs:
            transaction = doc.to_dict()
            transaction['id'] = doc.id  # Include the transaction ID in the response
            transactions.append(transaction)
            

        return jsonify({"transactions": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/api/Scheduled', methods=['POST'])
def schedule_transaction():
    try:
        data = request.get_json()
        product_name = data.get('Name')
        amount = data.get('Amount')
        price = data.get('Price')
        date = data.get('Date')
        transaction_type = data.get('Type')

        # Validate input data here if necessary
        transaction_type = int(transaction_type)

        ID = str(uuid.uuid4())

        # Add transaction to Firestore based on Type with current system time
        transaction_data = {
            'ID': ID,
            'Date': date,
            'Name': product_name,
            'Amount': amount,
            'Price': price,
            'Type': transaction_type
        }
        
        transaction_ref = db.collection('Scheduled').add(transaction_data)
        

        return jsonify({"message": "Transaction added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 50

    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
