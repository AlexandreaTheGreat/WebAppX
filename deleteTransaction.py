from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firestore with your credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/ALEXANDREA/WebAppX/cred.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/api/Transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Delete transaction from Firestore using transaction_id
        transaction_ref = db.collection('Transactions').document(transaction_id)
        transaction_ref.delete()

        return jsonify({"message": "Transaction deleted successfully"+transaction_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
