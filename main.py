import requests
import pymysql.cursors

# Fetch data from the API
api_url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(api_url)
data = response.json()

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="ella-bear004", #Add your password
    database="blog" 
    # i created a databse called blog
    # in mysql workbench and i imported the sql file from the folder into the database
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    )
""")

# Insert data into the table
for user in data:
    cursor.execute("""
        INSERT INTO users (id, name, email) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email)
    """, (user["id"], user["name"], user["email"]))

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted into MySQL database.")
