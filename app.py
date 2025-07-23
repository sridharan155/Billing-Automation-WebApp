from io import BytesIO
import gridfs
from flask import Flask, render_template, request, flash,jsonify,send_file
from pymongo import MongoClient
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key = 'your_secret_key'

MONGO_URI = "mongodb+srv://roshan_rithik:beeeDB@beee-project.jshar.mongodb.net/"
DB_NAME = "Expenditure"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

# Allowed file extensions
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('signin.html')

@app.route('/login',methods=['POST'])
def login_action_signin_page():
    return render_template('login.html')

@app.route('/expenditure',methods=['GET','POST'])
def expenditure():
    return render_template('Expenditure.html')

@app.route('/login-submit', methods=['POST'])
def login():
    try:
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        collection = db['register']
        found = collection.find_one({'username': username}, {'_id': 0})

        if found is None:
            popup = 'User Doesnt exist!'
            return render_template('login.html', popup=popup)
        else:
            if found['password'] != password:
                popup = 'Invalid Password!'
                return render_template('login.html',popup=popup)

            else:
                popup='loggedin'
                return render_template('Expenditure.html',popup=popup)

    except Exception as e:
        popup='An error occured'
        print(e)
        return render_template('login.html',popup=popup)

@app.route('/signin', methods=['POST'])
def sign_up():
    try:
        if request.method == 'POST':
            user = request.form.get('user')
            email = request.form.get('email')
            password = request.form.get('password')
            empid=request.form.get('empid')
            print('user: ', user)
            print('email: ', email)
            print('empid: ', empid)
            print('Password :', password)

            users_collection = db["register"]
            user_data = {
                "username": user,
                "empid":empid,
                "email": email,
                "password": password
            }

            # Check if the user data is already stored in the database
            existing_user = users_collection.find_one({ "email": email})
            if existing_user:
                popup= "You are already signed up! Please login."
                return render_template('login.html')

            # If not, insert the new user data
            users_collection.insert_one(user_data)
            popup="signed success fully"
            return render_template('Expenditure.html')

        else:
            popup="Invalid request and no data is not stored"
            return render_template('signin.html')

    except Exception as e:
        return render_template('signin.html')

@app.route('/billing', methods=['POST'])
def bill_submit():
    try:
        # Get form data
        employee_number = request.form['empNo']
        employee_name = request.form['empName']
        bill_amount = request.form['billAmount']
        bill_date = request.form['billDate']
        expenditure_details = request.form['expenditure_details']
        expenditure_description = request.form['expenditure_description']

        # Store data in MongoDB
        billing_record = {
            'employee_number': employee_number,
            'employee_name': employee_name,
            'bill_amount': bill_amount,
            'bill_date': bill_date,
            'expenditure_details': expenditure_details,
            'expenditure_description': expenditure_description,
            'status':'SUBMITTED'
        }

        collection = db['data']
        collection.insert_one(billing_record)
        flash("Record successfully added", "success")
        return render_template('Expenditure.html')

    except Exception as e:
        print(f"Error during form submission: {e}")
        flash("Failed to submit the form", "error")
        popup="An error occurred"
        return render_template('Bill.html')

@app.route('/bill',methods=['GET','POST'])
def bill():
    try:
        collection=db['data']
        records=list(collection.find())
        return render_template('Bill.html',records=records)
    except Exception as e:
        print(e)
        return render_template('Bill.html')

if __name__=='__main__':
    app.run(debug=True)