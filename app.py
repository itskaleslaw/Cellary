from flask import Flask, render_template, request, redirect, url_for, session
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="4GpS4lIdfoR9rQaklxq6"
)

MODEL_ID = "grocery-product-detection-s9z8d/1"
detected_items = {}
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        result = CLIENT.infer(file_path, model_id=MODEL_ID)

        if 'predictions' in result and isinstance(result['predictions'], list):
            for pred in result['predictions']:
                item = pred['class']
                confidence = pred['confidence']
                if item in detected_items:
                    detected_items[item]['count'] += 1
                else:
                    detected_items[item] = {'count': 1, 'confidence': confidence}

        session['detected_items'] = detected_items

        return redirect(url_for('index'))

    return render_template('index.html')

@app.route("/inventory")
def inventory():
    # Retrieve detected items from session
    detected_items = session.get('detected_items', {})
    return render_template('inventory.html', result=detected_items)
@app.route("/recipes")
def recipes():
    return render_template('recipes.html')

if __name__ == "__main__":
    app.run(debug=True)
