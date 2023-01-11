import os
from io import BytesIO
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_file

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

    



# Route for uploading a new file
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"success": "File uploaded successfully"})

# Route for creating a new file
@app.route('/create', methods=['POST'])
def create_file():
    # Get the file data from the request
    file_data = request.get_json()
    # Write the file data to the server
    with open(file_data["filename"], "w") as f:
        f.write(file_data["content"])
    return jsonify({"success": "File created successfully"})

# Route for downloading a file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Check if the file exists
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"})

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
    return jsonify({"files": files})

# Route for deleting a file
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    # Check if the file exists
    if os.path.exists(filename):
        os.remove(filename)
        return jsonify({"success": "File deleted successfully"})
    else:
        return jsonify({"error": "File not found"})
if __name__ == '__main__':
    app.run(debug=True)