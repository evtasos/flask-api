import os
from io import BytesIO
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import send_file
from docxtpl import DocxTemplate
from datetime import datetime

UPLOAD_FOLDER = 'archive'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app = Flask(__name__, template_folder= '.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    #check if all parameters are given
    if not all(key in data for key in ('filename', 'recipient', 'am', 'year')):
        return jsonify({"error": "Missing required parameters"}), 400
    # check if the recipient field is a string
    if not isinstance(data.get('recipient'), str):
        return jsonify({"error": "recipient parameter should be a string"}), 400
    # check if the am field is an integer
    if not isinstance(data.get('am'), int):
        return jsonify({"error": "am parameter should be an integer"}), 400
    # check if the year field is an integer
    if not isinstance(data.get('year'), int):
        return jsonify({"error": "year parameter should be an integer"}), 400
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y")

    try:
        template = 'archive/'+data.get('filename')
        recipient = data.get('recipient')
        am = data.get('am')
        year = data.get('year')

        if not os.path.isfile(template):
            return jsonify({"error": f"{template} not found"}), 404
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
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Check if the file exists
    if os.path.exists(file_path):
        # Write the new file data to the server
        with open(file_path, "w") as f:
            f.write(file_data["content"])
        return jsonify({"success": "File modified successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

# Route for listing all files
@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files}), 200

# Route for deleting a file
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Check if the file exists
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({"success": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 400

# Route for handling teh case when the endpoint is not found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404    
if __name__ == '__main__':
    app.run()