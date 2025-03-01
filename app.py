from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for frontend requests

# Load the trained model
try:
    model = tf.keras.models.load_model("model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# Define class labels
class_labels = ["Cat", "Dog"]  # Now returns "Cat" or "Dog"


@app.route("/")
def index():
    return render_template("index.html")  # Ensure `index.html` exists in `templates/`


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    try:
        # Preprocess the image
        image = Image.open(io.BytesIO(file.read())).convert("RGB").resize((64, 64))
        image_array = np.array(image) / 255.0  # Normalize
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # Make prediction
        prediction = model.predict(image_array)

        # If binary classification
        predicted_class = class_labels[int(prediction[0][0] > 0.5)]
        confidence = float(prediction[0][0])

        return jsonify({'class': predicted_class, 'confidence': confidence})

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=False)
