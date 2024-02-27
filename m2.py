import random
import string
from flask import Flask, request, jsonify,render_template
import cv2
import numpy as np
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.environ.get('DATABASE_URL')
SUPABASE_KEY = os.environ.get('API_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def apply_watercolor_effect(input_img):
    # Apply watercolor effect
    watercolor_image = cv2.stylization(input_img, sigma_s=100, sigma_r=0.45)
    return watercolor_image


@app.route('/get', methods=['GET','POST'])
def get():
    return render_template('index.html')

    

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

    # Apply watercolor effect
    watercolor_image = apply_watercolor_effect(original_img)

    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    file_name = f'K_{random_string}.png'

    # Encode watercolor image to bytes
    _, buffer = cv2.imencode('.png', watercolor_image)
    watercolor_image_bytes = buffer.tobytes()

    # Upload the watercolor image to Supabase Storage
    response = supabase.storage.from_("testbucket").upload(file=watercolor_image_bytes, path=f'watercolor_images/{file_name}', file_options={"content-type": "image/png"})
    
    # Check if the upload was successful
    if response.status_code == 200:
        try:
            # Get the URL of the uploaded image
            res = supabase.storage.from_('testbucket').get_public_url(f'watercolor_images/{file_name}')
            return jsonify({'watercolor_image_url': res})
        except KeyError:
            return jsonify({'error': 'Failed to get URL of uploaded image from Supabase response'})
    else:
        return jsonify({'error': 'Failed to upload image to Supabase'})

if __name__ == '__main__':
    app.run(debug=True)
