from flask import Flask, request, jsonify
import pickle
import os
import joblib  # Importing joblib as an alternative loader if needed

app = Flask(__name__)

# Define paths to the model and vectorizer files
model_path = 'model/rf_new_model_1.3.2.pkl'
vectorizer_path = 'model/tfidf_vectorizer_1.3.2.pkl'

# Function to load the model and vectorizer
def load_pickle_file(file_path):
    """
    Attempt to load a pickle file and handle errors gracefully.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please check the path and ensure the file exists.")
    
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except pickle.UnpicklingError:
        raise ValueError(f"Failed to load the file: {file_path}. It might be corrupted or not a valid pickle file.")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred while loading {file_path}: {str(e)}")

# Try loading the model and vectorizer using pickle
try:
    model = load_pickle_file(model_path)
    print("Model loaded successfully using pickle.")
except ValueError as pickle_error:
    print(f"Error loading model: {pickle_error}")
    # If there's an error with pickle, attempt to load using joblib
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully using joblib as a fallback.")
    except Exception as joblib_error:
        raise ValueError(f"Failed to load model using both pickle and joblib. Error: {joblib_error}")

# Load the TF-IDF vectorizer
try:
    tfidf_vectorizer = load_pickle_file(vectorizer_path)
    print("TF-IDF Vectorizer loaded successfully using pickle.")
except ValueError as pickle_error:
    print(f"Error loading TF-IDF vectorizer: {pickle_error}")
    # If there's an error with pickle, attempt to load using joblib
    try:
        tfidf_vectorizer = joblib.load(vectorizer_path)
        print("TF-IDF Vectorizer loaded successfully using joblib as a fallback.")
    except Exception as joblib_error:
        raise ValueError(f"Failed to load TF-IDF vectorizer using both pickle and joblib. Error: {joblib_error}")

# Route to handle prediction requests
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Get email subject and body from the JSON request
    email_subject = data.get('subject', '')
    email_body = data.get('body', '')

    # Check if both fields are provided
    if not email_subject or not email_body:
        return jsonify({'error': 'Please provide both email subject and body for prediction.'}), 400

    # Combine subject and body for vectorization
    combined_text = email_subject + " " + email_body

    # Transform the text using the loaded TF-IDF vectorizer
    try:
        transformed_text = tfidf_vectorizer.transform([combined_text])
    except Exception as e:
        return jsonify({'error': f'Failed to transform text. Error: {str(e)}'}), 500

    # Predict using the loaded model
    try:
        prediction = model.predict(transformed_text)
        result = 'Tread Carefully, something seems fishy about it' if prediction[0] == "1" else 'It looks like a Legitimate Email'
    except Exception as e:
        return jsonify({'error': f'Failed to make a prediction. Error: {str(e)}'}), 500

    # Return the prediction result
    return jsonify({'prediction': result})

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)