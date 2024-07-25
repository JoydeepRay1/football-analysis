from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return redirect(url_for('process_file', filename=file.filename))
    return redirect(request.url)

@app.route('/process/<filename>')
def process_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Call the processing scripts here
    os.system(f"bash scripts/pipeline.sh {file_path} output known_face_embeddings.npy known_face_names.npy")
    # Return the results
    return "Processing complete. Check the output folder."

if __name__ == "__main__":
    app.run(debug=True)
