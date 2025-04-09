import requests

url = "http://127.0.0.1:5000/predict"
image_data = "your_base64_encoded_image_here"  # Replace with actual Base64

response = requests.post(url, json={"image": image_data})
print(response.json())
