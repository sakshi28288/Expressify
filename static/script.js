const video = document.getElementById('video');
const emotionDisplay = document.getElementById('emotion-result');
const movieList = document.getElementById('movies');
const quoteBox = document.getElementById('quote-box');
const musicBox = document.getElementById('music-box');
const captureBtn = document.getElementById('capture-btn');

const bgMusic = new Audio();
bgMusic.loop = true;

// Start webcam on page load
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => console.error("Camera access denied:", err));

// Emotion detection
captureBtn.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const base64Image = canvas.toDataURL('image/jpeg');

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: base64Image })
  })
    .then(response => response.json())
    .then(data => {
      const emotion = data.emotion;
      emotionDisplay.textContent = `Detected Emotion: ${emotion}`;
      displayMovieRecommendations(emotion);
      playMusic(emotion);
      showQuote(emotion);
    })
    .catch(error => console.error("Error predicting emotion:", error));
});

// Fetch and display movie recommendations
function displayMovieRecommendations(emotion) {
  fetch(`/api/get-movies?emotion=${emotion}`)
    .then(response => response.json())
    .then(data => {
      movieList.innerHTML = ''; // Clear old recommendations
      data.movies.forEach(movie => {
        const div = document.createElement('div');
        div.className = 'movie';
        div.innerHTML = `
          <img src="${movie.poster}" alt="${movie.title}">
          <h3>${movie.title}</h3>
          <p>${movie.description}</p>
        `;
        movieList.appendChild(div);
      });
    })
    .catch(err => console.error("Failed to fetch movie recommendations:", err));
}

// Mood-based music
function playMusic(emotion) {
  const musicMap = {
    happy: 'https://www.bensound.com/bensound-music/bensound-happyrock.mp3',
    sad: 'https://www.bensound.com/bensound-music/bensound-slowmotion.mp3',
    angry: 'https://www.bensound.com/bensound-music/bensound-actionable.mp3',
    surprise: 'https://www.bensound.com/bensound-music/bensound-dubstep.mp3',
    neutral: 'https://www.bensound.com/bensound-music/bensound-goinghigher.mp3'
  };
  bgMusic.src = musicMap[emotion] || '';
  bgMusic.play();
  musicBox.innerText = `🎵 Mood Music: Playing something for your ${emotion} vibes...`;
}

// Mood-based quote
function showQuote(emotion) {
  const quotes = {
    happy: "Keep smiling, it makes people wonder what you're up to.",
    sad: "Every storm runs out of rain.",
    angry: "For every minute you are angry you lose sixty seconds of happiness.",
    surprise: "Surprise is the greatest gift which life can grant us.",
    neutral: "Balance is not something you find, it's something you create."
  };
  quoteBox.textContent = `💬 Quote: "${quotes[emotion] || 'Express yourself freely!'}"`;
}

// Real-time clock
function updateClock() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString();
  document.getElementById('clock').innerText = `🕒 Current Time: ${timeStr}`;
}
setInterval(updateClock, 1000);
updateClock();
