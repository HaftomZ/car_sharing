import sqlite3
from datetime import datetime, timedelta
from config.Hash import Hash

# Connect to SQLite database
conn = sqlite3.connect('hrin.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# ____________ Filling the User table ______________
# SQL query to insert data
insert_query_users = '''
INSERT INTO users (id, user_name, email, password, about, avatar, phone_number, average_rating)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of reviews with different date values
def generate_users():
    users = []

    for i in range(1, 16):
        id = i
        user_name = f"name{i}"
        email = f"{user_name}@gmail.com"
        password = Hash.bcrypt(f"name{i}_password")
        about = f'User number {i}'
        avatar = f'Nice picture {i}'
        phone_number = f'+31{i}3{i}34{i}'
        average_rating = (i % 5) + 1
        users.append((id, user_name, email, password, about, avatar, phone_number, average_rating))
    return users

data_1 = generate_users()

# Insert data into the table
cursor.executant(insert_query_users, data_1)

# Commit the transaction to save the changes
conn.commit()
cursor.execute("SELECT * FROM users")
# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)


# ____________ Filling the Review table ______________


# SQL query to insert data
insert_query_reviews = '''
INSERT INTO reviews (id, receiver_id, creator_id, created_at, rating, text_description)
VALUES (?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of reviews with different date values
def generate_reviews():
    reviews = []
    base_date = datetime(2025, 2, 24, 14, 45, 50)  # Starting date and time

    for i in range(1, 16):
        review_id = i
        receiver_id = (i % 3) + 1
        creator_id = ((i + 1) % 3) + 1
        rating = (i % 5) + 1
        text_description = f'Review {i}: ' + ('Really good' if rating == 5 else
                                                  'Nice' if rating == 4 else
                                                  'Neutral' if rating == 3 else
                                                  'Bad' if rating == 2 else 'Really bad')

        # Increment the base date by a few seconds for each review
        review_date = base_date + timedelta(seconds=i * 15)  # Increments by 15 seconds

        reviews.append(
            (review_id, receiver_id, creator_id, review_date.strftime('%Y-%m-%d %H:%M:%S'), rating, text_description))

    return reviews


data_2 = generate_reviews()

# Insert data into the table
cursor.executemany(insert_query_reviews, data_2)

# Commit the transaction to save the changes
conn.commit()

cursor.execute("SELECT * FROM reviews")

# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)


# ____________ Filling the Booking table ______________


# SQL query to insert data
insert_query_reviews_3 = '''
INSERT INTO bookings (booking_id, booker_id, trip_id, status, adult_seats, children_seats, created_at, updated_at, pickup_location)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)




# Function to generate a list of reviews with different date values
def generate_bookings():
    bookings = []
    base_date = datetime(2025, 2, 24, 14, 45, 50)  # Starting date and time

    for i in range(1, 16):
        booking_id = i
        booker_id = (i % 5) + 1
        trip_id = ((i + 1) % 3) + 1
        status = "Pending"
        adult_seats = ((i + 1) % 3) + 1
        children_seats = ((i + 1) % 3) + 1
        pickup_location = f'Pickup location {i}'
        end_location = f'End location {i}'


        # Increment the base date by a few seconds
        created_at = base_date + timedelta(seconds=i * 15)  # Increments by 15 seconds
        updated_at = base_date + timedelta(hours=i)  # Increments by 10 seconds

        bookings.append((booking_id, booker_id, trip_id, status, adult_seats, children_seats, created_at.strftime('%Y-%m-%d %H:%M:%S'), updated_at.strftime('%Y-%m-%d %H:%M:%S'), pickup_location))


    return bookings


data_3 = generate_bookings()

# Insert data into the table
cursor.executemany(insert_query_reviews_3, data_3)

# Commit the transaction to save the changes
conn.commit()

cursor.execute("SELECT * FROM reviews")

# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)

# ____________ Filling the Cars table ______________


# SQL query to insert data
insert_query_reviews_4 = '''
INSERT INTO cars (owner_id, id, model, year, adult_seats, children_seats, smoking_allowed, wifi_available, air_conditioning, pet_friendly, car_status, car_availability_status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of cars with different date values
def generate_cars():
    cars = []

    for i in range(1, 16):
        id = i
        owner_id = (i % 5) + 1
        year = 2010+i
        model = f'BMW {i}'
        adult_seats = ((i + 1) % 3) + 1
        children_seats = ((i + 1) % 3) + 1
        smoking_allowed = True
        wifi_available = True
        air_conditioning = True
        pet_friendly = False
        car_status = "approved"
        car_availability_status = "available"

        cars.append((owner_id, id, model, year, adult_seats, children_seats, smoking_allowed, wifi_available, air_conditioning, pet_friendly, car_status, car_availability_status))

    return cars


data_4 = generate_cars()

# Insert data into the table
cursor.executemany(insert_query_reviews_4, data_4)

# Commit the transaction to save the changes
conn.commit()

cursor.execute("SELECT * FROM cars")

# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)


# ____________ Filling the Trips table ______________


# SQL query to insert data
insert_query_reviews_5 = '''
INSERT INTO trips (id, creator_id, car_id, departure_location, destination_location, departure_time, arrival_time, available_adult_seats, available_children_seats, status, passengers_count, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''


# Function to generate a list of trips with different date values
def generate_trips():
    trips = []
    base_date = datetime(2025, 2, 24, 14, 45, 50)  # Starting date and time

    for i in range(1, 16):
        id = i
        creator_id = (i % 5) + 1
        car_id = ((i + 1) % 3) + 1
        departure_location = f"Location {i}"
        destination_location = f"Location {i+3}"
        departure_time = base_date + timedelta(days=i)
        arrival_time = base_date + timedelta(hours=i, minutes=i)
        available_adult_seats = ((i + 1) % 3) + 1
        available_children_seats = ((i + 1) % 3) + 1
        passengers_count = ((i + 1) % 3) + 1
        status = "Open"
        # Increment the base date by a few seconds
        created_at = base_date + timedelta(seconds=i * 15)  # Increments by 15 seconds
        updated_at = base_date + timedelta(hours=i)  # Increments by 10 seconds

        trips.append((id, creator_id, car_id, departure_location, destination_location, departure_time.strftime('%Y-%m-%d %H:%M:%S'), arrival_time.strftime('%Y-%m-%d %H:%M:%S'), available_adult_seats, available_children_seats, status, passengers_count, created_at.strftime('%Y-%m-%d %H:%M:%S'), updated_at.strftime('%Y-%m-%d %H:%M:%S')))

    return trips


data_5 = generate_trips()

# Insert data into the table
cursor.executemany(insert_query_reviews_5, data_5)

# Commit the transaction to save the changes
conn.commit()

cursor.execute("SELECT * FROM trips")

# Query the database to verify the data
rows = cursor.fetchall()

# Print all records in the table
for row in rows:
    print(row)

# Close the connection to the database
conn.close()

