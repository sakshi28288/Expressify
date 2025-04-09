from flask import Flask, request, jsonify, render_template
import cv2
import tensorflow as tf
import numpy as np
import base64
import logging
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

logging.basicConfig(level=logging.INFO)

# Load model
try:
    model = tf.keras.models.load_model('emotiondetector.h5')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

emotions = ["Anger", "Neutral", "Fear", "Happy", "Sadness", "Surprise", "Neutral"]
OMDB_API_KEY = '1769e094'

# Emotion to genre mapping
emotion_keywords = {
    'happy': 'comedy',
    'sadness': 'drama',
    'anger': 'action',
    'surprise': 'thriller',
    'neutral': 'family',
    'fear': 'horror',
    'neutral': 'mystery'
}

# Fallback movie data
fallback_movies = {
    "happy": [
        {
            "title": "Inside Out",
            "description": "A joyful journey through emotions.",
            "poster": "https://m.media-amazon.com/images/I/71xBLRBYOiL._AC_UF1000,1000_QL80_.jpg"
        },
        {
            "title": "Zindagi Na Milegi Dobara",
            "description": "Feel-good film about friendship & self-discovery.",
            "poster": "https://m.media-amazon.com/images/I/51tJL0CK6ZL.jpg"
        }
    ],
    "sadness": [
        {
            "title": "The Pursuit of Happyness",
            "description": "Inspiring story of a father's struggle and love.",
            "poster": "https://m.media-amazon.com/images/I/51wpY7Z3Y0L._AC_UF894,1000_QL80_.jpg"
        },
        {
            "title": "Taare Zameen Par",
            "description": "Emotional story of a misunderstood child.",
            "poster": "https://m.media-amazon.com/images/I/81AHF8+H1wL._AC_UF1000,1000_QL80_.jpg"
        }
    ],
    "anger": [
        {
            "title": "Gladiator",
            "description": "A tale of revenge, power, and honor.",
            "poster": "https://m.media-amazon.com/images/I/51j0BWlZ5pL.jpg"
        },
        {
            "title": "Dangal",
            "description": "A determined father trains his daughters.",
            "poster": "https://m.media-amazon.com/images/I/81wxP99doKL._AC_UF1000,1000_QL80_.jpg"
        }
    ]
}

def decode_image(image_data):
    try:
        img_data = base64.b64decode(image_data.split(",")[1])
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logging.error(f"Error decoding image: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("⚡ /predict API hit!")

    if model is None:
        print("❌ Model not loaded")
        return jsonify({"error": "Model not loaded properly."}), 500

    try:
        data = request.json
        print("📷 Data keys received:", data.keys())

        img_data = data.get('image', None)
        if img_data is None:
            print("❌ No image provided.")
            return jsonify({"error": "No image provided."}), 400

        img = decode_image(img_data)
        if img is None:
            print("❌ Failed to decode image.")
            return jsonify({"error": "Invalid image format."}), 400

        print("✅ Image decoded successfully.")
        img = cv2.resize(img, (48, 48))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=-1)
        img = np.expand_dims(img, axis=0)

        predictions = model.predict(img)
        print("✅ Model prediction:", predictions)

        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_emotion = emotions[predicted_class].lower()
        print(f"🎭 Predicted Emotion: {predicted_emotion}")

        return jsonify({"emotion": predicted_emotion})

    except Exception as e:
        print(f"❌ Exception during prediction: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-movies')
def get_movies():
    emotion = request.args.get('emotion', '').lower()
    keyword = emotion_keywords.get(emotion, 'drama')
    movies = []

    try:
        response = requests.get(f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={keyword}")
        data = response.json()

        if data.get('Response') == 'True':
            for item in data.get('Search', [])[:9]:  # Top 9
                movies.append({
                    "title": item.get('Title'),
                    "year": item.get('Year'),
                    "poster": item.get('Poster'),
                    "description": f"A recommended {keyword} movie."
                })
            return jsonify({"movies": movies})
        else:
            print("⚠️ OMDb returned no results, using fallback.")
            return jsonify({"movies": fallback_movies.get(emotion, [])})

    except Exception as e:
        print(f"❌ OMDb API error: {e}")
        return jsonify({"movies": fallback_movies.get(emotion, [])})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
