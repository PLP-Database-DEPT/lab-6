import requests
import pymysql.cursors

# Fetch data from the API
api_url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(api_url)
data = response.json()

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="ella-bear004", # Add your password
    database="blog" 
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INT PRIMARY KEY,
        title VARCHAR(255),
        body TEXT,
        userId INT,
        FOREIGN KEY(userId) REFERENCES users(id)
    )
""")

# Insert data into the table
for post in data:
    cursor.execute("""
        INSERT INTO posts (id, title, body, userId) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title = VALUES(title), body = VALUES(body), userId = VALUES(userId)
    """, (post["id"], post["title"], post["body"], post["userId"]))

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted into MySQL database.")
