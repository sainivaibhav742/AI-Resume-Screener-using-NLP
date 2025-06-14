# In app.py
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from model.resume_matcher import match_resume  # This must return a dictionary

# Initialize Flask app
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file part", 400

    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            result = match_resume(file_path)  # ✅ Ensure you're passing only 1 argument
            return render_template('result.html', result=result)
        except Exception as e:
            return f"Error processing resume: {str(e)}", 500
    else:
        return "Invalid file type. Only PDF and DOCX are allowed.", 400

if __name__ == '__main__':
    app.run(debug=True)
