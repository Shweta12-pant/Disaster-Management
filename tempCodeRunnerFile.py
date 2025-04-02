    try:
        conn = mysql.connector.connect(
            host="localhost",  # Use the correct host
            user="root",
            password="your_password",
            database="your_database"
        )
        print("Connected successfully!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")