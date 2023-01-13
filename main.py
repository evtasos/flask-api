import os
from io import BytesIO
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import send_file
from docxtpl import DocxTemplate
from datetime import datetime

UPLOAD_FOLDER = 'archive'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__, template_folder= '.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#     return render_template('index.html')

# Route for uploading a new file
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = filename.rpartition('_')[2] 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"success": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400        

# Route for creating a new file
@app.route('/create', methods=['POST'])
def create_file():
    data = request.get_json()
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y")

    try:
        template = 'archive/'+data.get('filename')
        recipient = data.get('recipient')
        am = data.get('am')
        year = data.get('year')

        doc = DocxTemplate(template)
        context = { 'recipient' : recipient, 'am' : am, 'year' : year}
        doc.render(context)
        filename, file_extension = os.path.splitext(template)
        doc.save(f"{filename}_{recipient}_{dt_string}{file_extension}")
        return jsonify({"success": f"File created successfully with name {filename}_{recipient}_{dt_string}{file_extension}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Route for downloading a file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Check if the file exists
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True), 200
    else:
        return jsonify({"error": "File not found"}), 400

# Route for modifying a file
@app.route('/modify/<filename>', methods=['PUT'])
def modify_file(filename):
    # Get the new file data from the request
    file_data = request.get_json()
    # Check if the file exists
    if os.path.exists(filename):
        # Write the new file data to the server
        with open(filename, "w") as f:
            f.write(file_data["content"])
        return jsonify({"success": "File modified successfully"})
    else:
        return jsonify({"error": "File not found"})

# Route for listing all files
@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files}), 200

# Route for deleting a file
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({"success": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 400
    
if __name__ == '__main__':
    app.run(debug=True)