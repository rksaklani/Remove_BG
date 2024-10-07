from flask import Flask, request, send_file, render_template, jsonify
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        # Ensure image file is present in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        # Open the image using PIL
        input_image = Image.open(file.stream)

        # Convert image to 'RGBA' mode if it's not in an accepted mode
        if input_image.mode not in ['RGBA', 'RGB']:
            input_image = input_image.convert('RGBA')

        # Remove the background
        output_image = remove(input_image)

        # Save to an in-memory file (BytesIO)
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Send the file back as a PNG download
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output_image.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
