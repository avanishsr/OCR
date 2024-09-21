from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path

# Initialize Flask app
app = Flask(__name__)

import pytesseract
import os

try:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
except Exception as e:
    print("Tesseract not found. Please install it or check your path.")

if not os.path.exists('uploads'):
    os.makedirs('uploads')


# Route to upload file (PDF or image) and perform OCR
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    extracted_text = ""

    if file:
        # Save file to a temporary path
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Check if the file is a PDF
        if file.filename.lower().endswith('.pdf'):
            # Convert PDF to images
            images = convert_from_path(file_path)
            for img in images:
                text = pytesseract.image_to_string(img)
                extracted_text += text + "\n"
        else:
            # Handle image files directly
            img = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(img)

        # Return the extracted text
        return jsonify({"extracted_text": extracted_text})


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
