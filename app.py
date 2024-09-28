from flask import Flask, render_template, request
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Create this folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="4GpS4lIdfoR9rQaklxq6"
)

MODEL_ID = "grocery-product-detection-s9z8d/1"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        result = CLIENT.infer(file_path, model_id=MODEL_ID)
        textResult = ""
        for pred in result['predictions']:
            textResult += f"{pred['class']}: {pred['confidence']}\n"
    return render_template('index.html', result=textResult)

@app.route('/upload', methods=['POST'])
def upload_file():
    result = None
    if 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        result = CLIENT.infer(file_path, model_id=MODEL_ID)
    return render_template('upload_result.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)