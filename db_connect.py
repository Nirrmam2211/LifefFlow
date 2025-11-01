import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="student_db"
)
cursor = conn.cursor()

# Insert a new student record
cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", ("Frank", 21, "B"))
conn.commit()

# Fetch and display all records
cursor.execute("SELECT * FROM students")
for (id, name, age, grade) in cursor.fetchall():
    print(f"ID: {id}, Name: {name}, Age: {age}, Grade: {grade}")

# Update a student's grade
cursor.execute("UPDATE students SET grade = %s WHERE name = %s", ("A+", "Bob"))
conn.commit()

# Delete a student record
cursor.execute("DELETE FROM students WHERE name = %s", ("Dave",))
conn.commit()

# Close connection
cursor.close()
conn.close()
