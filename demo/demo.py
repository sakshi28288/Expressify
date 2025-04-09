import cv2
import numpy as np
from keras.models import model_from_json
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Load trained model
json_file = open("emotiondetector.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("emotiondetector.h5")

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Emotion labels
labels = {0: 'Angry', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad'}

# Function to preprocess face for model input
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)  # Reshape to match model input
    return feature / 255.0  # Normalize pixel values

# Function to detect emotion from image
def detect_emotion(image_data):
    # Decode the image data from base64
    img_data = base64.b64decode(image_data.split(',')[1])
    img = Image.open(BytesIO(img_data))
    img = np.array(img.convert('L'))  # Convert to grayscale

    # Detect faces and predict emotion
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
    final_emotion = "No Emotion Detected"
    for (x, y, w, h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))  # Resize for model input
        face = extract_features(face)  # Preprocess

        pred = model.predict(face)
        emotion = labels[int(pred.argmax())]  # Convert np.int64 to int
        final_emotion = emotion  # Store final emotion

    return final_emotion

# API to analyze emotion from image
@app.route('/api/analyze-emotion', methods=['POST'])
def analyze_emotion():
    data = request.get_json()
    image_data = data['image']
    
    # Get the emotion from the image
    emotion = detect_emotion(image_data)
    
    # Return detected emotion as response
    return jsonify({'emotion': emotion})

# API to get movie recommendations based on emotion
@app.route('/api/get-movies', methods=['GET'])
def get_movies():
    emotion = request.args.get('emotion')
    # Add movie recommendations logic based on detected emotion
    # For now, just returning a mock list based on the emotion
    if emotion == 'Happy':
        movies = [{"title": "The Pursuit of Happyness", "poster": "https://image.tmdb.org/t/p/w500/pYWW0XlCFD5kZ69gjFyYYV59DgV.jpg", "description": "A motivational drama."}]
    else:
        movies = [{"title": "Finding Nemo", "poster": "https://image.tmdb.org/t/p/w500/qk64JgdMRzpzvAkmb83fmQFVpR.jpg", "description": "A heartwarming animated adventure."}]
    
    return jsonify({'movies': movies})

if __name__ == '__main__':
    app.run(debug=True)
