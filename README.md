# 🎭 ExpressiFy – Emotion-Based Movie & Music Recommendation System

ExpressiFy is an AI-powered web application that detects a user's real-time **facial emotion** through a webcam and recommends personalized **movies** or **music** accordingly. It uses **Deep Learning** with **CNN**, real-time webcam input, and the **OMDb API** to suggest content that matches the user’s current mood.

---

## 📸 Features

- 🔍 Real-time Emotion Detection using webcam
- 🧠 Deep Learning-based Facial Expression Recognition (CNN)
- 🎬 Emotion-Based Movie & Music Recommendation
- 🌐 Flask Backend + HTML/CSS/JavaScript Frontend
- 🧩 Integration with [OMDb API](https://www.omdbapi.com/) for real-time movie data
- 💡 Clean, interactive UI with a live webcam feed and results display

---

## 🛠️ Tech Stack

| Component      | Technology Used                  |
|----------------|----------------------------------|
| Frontend       | HTML, CSS, JavaScript            |
| Backend        | Python, Flask                    |
| Machine Learning | TensorFlow, Keras (CNN model)  |
| Emotion Model  | Trained on FER-2013 Dataset      |
| Webcam Access  | JavaScript (WebRTC API)          |
| External API   | OMDb API for movie recommendations |
| Image Processing | OpenCV, PIL, NumPy             |

---

## 📂 Project Structure

```
ExpressiFy/
│
├── expressify_backend/
│   ├── app.py               # Flask backend
│   ├── emotiondetector.h5   # Trained emotion model
│   ├── emotiondetector.json # (Optional) Model config
│   ├── demo.py              # Backup testing script
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── style.css            # Stylesheet
│   └── script.js            # JavaScript for webcam + API calls
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ExpressiFy.git
cd ExpressiFy
```

### 2. Create a Python Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r expressify_backend/requirements.txt
```

> ⚠️ If you face version conflicts, manually adjust the TensorFlow, NumPy, etc. versions.
> If you want to RUN the project download this file  
https://drive.google.com/file/d/1iZB2ZM1aMfARL0qv0BZn-YT2gKbgykdU/view?usp=drive_link
### 4. Run the Flask App
```bash
cd expressify_backend
python app.py
```

The server will start at `http://127.0.0.1:5001`

### 5. Open the Frontend
Open `frontend/index.html` in your browser, or copy it into Flask templates and integrate routes.

---

## 🎮 How It Works

1. User opens the web page → Camera activates
2. User clicks **"Detect Emotion"**
3. Captured image is sent to Flask backend via JavaScript `fetch()`
4. Flask loads the CNN model, predicts the emotion
5. Detected emotion is returned to frontend
6. OMDb API is queried for movies related to that emotion
7. Results are displayed instantly on the page

---

## 📈 Future Enhancements

- Add text sentiment + voice-based emotion detection
- Support Spotify API for real music recommendations
- Use Transfer Learning for better accuracy (e.g., ResNet, MobileNet)
- Store user emotion history in database for analytics

---

## 📄 License

This project is for educational purposes and part of a college academic submission.

---

## 👥 Authors

- Sakshi Sinha –-
- Janavi Singh -- 

---

## 🙌 Special Thanks

- [FER-2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)
- [OMDb API](https://www.omdbapi.com/)
- Faculty support

```
