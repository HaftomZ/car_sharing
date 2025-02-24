import sqlite3
from datetime import datetime, timedelta
# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('hrin.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

##____________ Filling the User table ______________
# SQL query to insert data
insert_query = '''
INSERT INTO users (id, user_id, creator_id, created_at, mark, text_description)
VALUES (?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of 10 reviews with different date values
def generate_reviews():
    reviews = []
    base_date = datetime(2025, 2, 24, 14, 45, 50)  # Starting date and time

    for i in range(1, 10):
        review_id = i  # Review ID increments
        user_id = (i % 3) + 1  # Random user ID between 1 and 3
        creator_id = ((i + 1) % 3) + 1  # Random creator ID between 1 and 3
        mark = (i % 5) + 1  # Random mark between 1 and 5
        text_description = f'Review {i + 1}: ' + ('Really good' if mark == 5 else
                                                  'Nice' if mark == 4 else
                                                  'Neutral' if mark == 3 else
                                                  'Bad' if mark == 2 else 'Really bad')

        # Increment the base date by a few seconds for each review
        review_date = base_date + timedelta(seconds=i * 15)  # Increments by 15 seconds

        reviews.append(
            (review_id, user_id, creator_id, review_date.strftime('%Y-%m-%d %H:%M:%S'), mark, text_description))

    return reviews


# Generate the reviews
data = generate_reviews()

# Insert data into the table
cursor.executemany(insert_query, data)

# Commit the transaction to save the changes
conn.commit()





##____________ Filling the Review table ______________

# SQL query to insert data
insert_query = '''
INSERT INTO reviews (id, user_id, creator_id, created_at, mark, text_description)
VALUES (?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of 10 reviews with different date values
def generate_reviews():
    reviews = []
    base_date = datetime(2025, 2, 24, 14, 45, 50)  # Starting date and time

    for i in range(1, 10):
        review_id = i  # Review ID increments
        user_id = (i % 3) + 1  # Random user ID between 1 and 3
        creator_id = ((i + 1) % 3) + 1  # Random creator ID between 1 and 3
        mark = (i % 5) + 1  # Random mark between 1 and 5
        text_description = f'Review {i + 1}: ' + ('Really good' if mark == 5 else
                                                  'Nice' if mark == 4 else
                                                  'Neutral' if mark == 3 else
                                                  'Bad' if mark == 2 else 'Really bad')

        # Increment the base date by a few seconds for each review
        review_date = base_date + timedelta(seconds=i * 15)  # Increments by 15 seconds

        reviews.append(
            (review_id, user_id, creator_id, review_date.strftime('%Y-%m-%d %H:%M:%S'), mark, text_description))

    return reviews


# Generate the reviews
data = generate_reviews()

# Insert data into the table
cursor.executemany(insert_query, data)

# Commit the transaction to save the changes
conn.commit()



# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)

# Close the connection to the database
conn.close()

