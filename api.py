from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Firestore with your credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/ALEXANDREA/Food-Recipe-App-React-Native/weathereats.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/api/HotandHumid', methods=['GET'])
def get_all_recipes():
    try:
        # Retrieve recipes from Firestore
        recipes = []
        recipe_docs = db.collection('Hot and Humid').stream()

        for doc in recipe_docs:
            recipe = doc.to_dict()
            recipe['id'] = doc.id  # Include the recipe ID in the response
            recipes.append(recipe)
            

        return jsonify({"recipes": recipes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "This is a test endpoint"})

    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)