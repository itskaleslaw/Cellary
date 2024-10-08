from flask import Flask, render_template, request, redirect, url_for, session
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="4GpS4lIdfoR9rQaklxq6"
)

MODEL_ID = "grocery-product-detection-s9z8d/1"
inventory_items = {}
detected_items = {}
temporary_items = {}

@app.route("/", methods=["GET", "POST"])
def index():
    detected_items = session.get('detected_items', {})
    temporary_items = {}
    confirm_message_manual = ""
    if request.method == "POST":
        if 'file' in request.files:
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
                    
                    if item in temporary_items:
                        temporary_items[item]['count'] += 1
                    else:
                        temporary_items[item] = {'count': 1, 'confidence': confidence}

            session['detected_items'] = detected_items
            session['temporary_items'] = temporary_items

            return render_template('index.html', result=temporary_items)

        else:
            item = request.form['manual_items']
            detected_items = session.get('detected_items', {})
            manual_quantity = int(request.form.get('manual_quantity', 1))
            
            if item in detected_items:
                detected_items[item]['count'] += manual_quantity
            else:
                detected_items[item] = {'count': manual_quantity, 'confidence': 1.0}
            
            confirm_message_manual = f"Added {manual_quantity} of {item} to the inventory."

            session['detected_items'] = detected_items

            return render_template('index.html', result="blank", confirm_message_manual=confirm_message_manual)

    temporary_items = session.get('temporary_items', {})
    return render_template('index.html', result=temporary_items)

@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    detected_items = session.get('detected_items', {})
    session['detected_items'] = {}
    for item in detected_items.keys():
        if item in inventory_items.keys():
            value = detected_items.get(item).get('count') + inventory_items.get(item)
            inventory_items.update({item: value})
        else:
            inventory_items.update({item: detected_items.get(item).get('count')})
        print(inventory_items.get(item))
    if request.method == "POST":
        name = request.form.get('food')
        num = int(request.form.get('quantity'))
        if name in inventory_items.keys():
            value = num + inventory_items.get(name)
            if value <= 0:
                inventory_items.pop(name)
            else:
                inventory_items.update({name: value})
        else:
            if num > 0:
                inventory_items.update({name: num})
        print(inventory_items.get(name))
        detected_items = {}
    detected_items = {}
    return render_template('inventory.html', result=inventory_items)

@app.route("/recipes")
def recipes():
    return render_template('recipes.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
