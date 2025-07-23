import gridfs
from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from io import BytesIO

# Flask app to run the web-app
app = Flask(__name__)

# Connecting to MongoDB database
client = MongoClient("mongodb+srv://roshan_rithik:beeeDB@beee-project.jshar.mongodb.net/")
db = client["Expenditure"]
fs = gridfs.GridFS(db)

# Allowed file extensions
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Default HTML Template
app.template_folder = 'C:\\Users\\suren\\PycharmProjects\\BEE sir PROJECT\\template'

@app.route('/')
def home():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Save file to GridFS
        file_id = fs.put(file, filename=filename)

        return jsonify({"success": True, "file_id": str(file_id)}), 201

    return jsonify({"error": "File type not allowed"}), 400

# Route to retrieve a file from GridFS
@app.route('/file/<file_id>', methods=['GET'])
def get_file(file_id):
    try:
        grid_out = fs.get(file_id)
        return send_file(BytesIO(grid_out.read()), attachment_filename=grid_out.filename, mimetype=grid_out.content_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
