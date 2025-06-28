import os
from flask import Flask, render_template, request
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_bw(image_path):
    image = Image.open(image_path)
    img_arr = np.array(image)

    # If grayscale, the image array will have only 2 dimensions (H x W)
    if len(img_arr.shape) == 2:
        return True
    elif len(img_arr.shape) == 3 and img_arr.shape[2] == 1:
        return True
    else:
        # Convert to grayscale and back, compare with original
        gray_image = image.convert("L")
        gray_back_to_rgb = gray_image.convert("RGB")
        return np.array_equal(np.array(image), np.array(gray_back_to_rgb))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file uploaded", 400
    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    result = "Black & White" if is_bw(filepath) else "Color"
    return render_template('index.html', filename=file.filename, result=result)

@app.route('/display/<filename>')
def display_image(filename):
    return f"/static/uploads/{filename}"

if __name__ == '__main__':
    app.run(debug=True)
