import os
import random
import string
from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('API_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def apply_watercolor_effect(input_img):
    # Apply watercolor effect
    watercolor_image = cv2.stylization(input_img, sigma_s=100, sigma_r=0.45)
    return watercolor_image
def apply_pencil_sketch_color(input_img):
    # Convert image to grayscale
    gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    # Invert grayscale image
    inv_gray_img = 255 - gray_img

    # Apply Gaussian blur to the inverted grayscale image with a larger kernel size
    blur_img = cv2.GaussianBlur(inv_gray_img, (111, 111), sigmaX=0, sigmaY=0)

    # Invert the blurred image
    inv_blur_img = 255 - blur_img

    # Apply dodge blend mode (enhanced division) to get the pencil sketch effect
    pencil_sketch = cv2.divide(gray_img, inv_blur_img, scale=256.0)

    return pencil_sketch



    
@app.route('/', methods=['POST'])
def index():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Check if the file is allowed
    if not file.content_type.startswith('image'):
        return jsonify({'error': 'Only image files are allowed'})

    # Read the image
    
    img_np = np.frombuffer(file.read(), np.uint8)
    original_img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)


    if 'ChangeType' in request.form and request.form['ChangeType'] == 'pencil':
        conv_img = apply_pencil_sketch_color(original_img)
    elif 'ChangeType' in request.form and request.form['ChangeType'] == 'water':
        conv_img = apply_watercolor_effect(original_img)
    else:
        return jsonify({'error': "ChangeType not provided or not in context"}), 400
        
    
    
    

    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    file_name = f'K_{random_string}.png'

    # Check if 'd' parameter is present in form data and set it to 'local'
    if 'StorageType' in request.form and request.form['StorageType'] == 'local':
        # Check if the folder exists, if not, create it
        if not os.path.exists('conv_imgs'):
            os.makedirs('conv_imgs')
        
        # Save the watercolor image locally
        local_path = f"conv_imgs/{file_name}"
        cv2.imwrite(local_path, conv_img)
        return jsonify({'image_url': request.host_url + local_path})

    # Upload the watercolor image to Supabase Storage
    _, buffer = cv2.imencode('.png', conv_img)
    watercolor_image_bytes = buffer.tobytes()
    response = supabase.storage.from_("testbucket").upload(file=watercolor_image_bytes, path=f'conv_imgs/{file_name}', file_options={"content-type": "image/png"})
    
    # Check if the upload was successful
    if response.status_code == 200:
        try:
            # Get the URL of the uploaded image
            res = supabase.storage.from_('testbucket').get_public_url(f'conv_imgs/{file_name}')
            return jsonify({'image_url': res})
        except KeyError:
            return jsonify({'error': 'Failed to get URL of uploaded image from Supabase response'})
    else:
        return jsonify({'error': 'Failed to upload image to Supabase'})

# Route to serve locally saved images
@app.route('/conv_imgs/<filename>')
def serve_image(filename):
    return send_from_directory('conv_imgs', filename)

if __name__ == '__main__':
    app.run(debug=True)
