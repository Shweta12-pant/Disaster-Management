import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",  # Use the correct host
        user="root",
        password="2511",
        database="disaster_relief"
    )
    print("Connected successfully!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")