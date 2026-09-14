from flask import Flask, render_template, request
import joblib
import os
from feature_extraction import extract_features

app = Flask(__name__, 
            template_folder="../frontend/templates",
            static_folder="../frontend/static")

# Load trained model
model = joblib.load("optimized_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]

    features = extract_features(url)
    prediction = model.predict(features)[0]

    if prediction == 1:
        result = "⚠ Phishing Website Detected!"
    else:
        result = "✅ Legitimate Website"

    return render_template("index.html", prediction_text=result)

if __name__ == "__main__":
    app.run(debug=True)
