from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from flask_cors import CORS 

app = Flask(__name__, template_folder='templates')
CORS(app)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '2511',  # Replace with your MySQL password
    'database': 'Disaster_Relief'
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Create tables if they do not exist
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Create volunteers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_type VARCHAR(50),
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(15),
            location VARCHAR(100),
            skills TEXT
        )
    """)
    
    # Create donations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            amount DECIMAL(10, 2),
            donation_type VARCHAR(50),
            payment_method VARCHAR(50)
        )
    """)
    
    # Create emergency_requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
            location VARCHAR(100),
            disaster_type VARCHAR(100),
            food_needed INT,
            casualties INT,
            shelter_type VARCHAR(100),
            comments TEXT
        )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()

# Call create_tables when the app starts
create_tables()

# Serve the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Serve the volunteer page
@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

# Serve the donation page
@app.route('/donation')
def donation():
    return render_template('donation.html')

# Serve the emergency request page
@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

# 📥 Volunteer Form Submission
@app.route('/submit-volunteer', methods=['POST'])  # Ensure POST is allowed
def submit_volunteer():
    try:
        data = request.json  # Get JSON data from request
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        location = data.get('location')
        skills = data.get('skills')

        if not all([name, email, phone, location, skills]):
            return jsonify({"error": "All fields are required"}), 400
    
        conn = mysql.connector.connect(
            host="your_host",
            user="your_user",
            password="your_password",
            database="your_database"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO volunteers (name, email, phone, location, skills) VALUES (%s, %s, %s, %s, %s)", 
                       (name, email, phone, location, skills))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Volunteer registered successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📥 Donation Form Submission
@app.route('/submit-donation', methods=['GET', 'POST'])
def handle_volunteer():
    if request.method == 'GET':
        return jsonify({"message": "Send a POST request to submit data"})

    elif request.method == 'POST':
        data = request.get_json()  # Get JSON data from request
        return jsonify({"message": "Volunteer submitted successfully", "data": data}) 
def submit_donation():
    name = request.form.get('name')
    age = request.form.get('age')
    amount = request.form.get('amount')
    donation_type = request.form.get('type')
    payment_method = request.form.get('payment_method')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO donations (name, age, amount, donation_type, payment_method)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, age, amount, donation_type, payment_method))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('donation'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📥 Emergency Request Form Submission
@app.route('/submit-emergency', methods=['POST'])
def submit_emergency():
    name = request.form.get('name')
    phone = request.form.get('phone')
    location = request.form.get('location')
    disaster_type = request.form.get('disaster')
    food_needed = request.form.get('food')
    casualties = request.form.get('casualties')
    shelter_type = request.form.get('shelter')
    comments = request.form.get('comments')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO emergency_requests (name, phone, location, disaster_type, food_needed, casualties, shelter_type, comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, phone, location, disaster_type, food_needed, casualties, shelter_type, comments))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('emergency'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
