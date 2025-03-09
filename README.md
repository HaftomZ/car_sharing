# HRIN

# 🚗 Trip Share App

A **trip-sharing** application built with **Python, FastAPI, OAuth2, and JWT**, following the **MVC architecture**. The app allows **passengers and drivers** to create and book trips, manage their profiles, and handle payments, while **admins** oversee platform operations.

## ✨ Features

### 🔹 Admin Panel (Super Admin & Moderator)
- Manage the entire application.
- Handle **payment & trip-related issues**.
- Access, create, update, and delete **users, trips, cars, and reviews**.

### 🔹 User Roles (Passenger & Driver)
- **Account Management:** Sign up, log in, update, delete, and verify accounts via email.
- **Profile Features:** Upload profile pictures.
- **Trip Management:** Create and book trips.
- **Car Management:** Add a car with details (model, year, available seats, smoking policy, etc.).
- **Reviews:** Leave and view reviews for drivers & passengers.
- **Booking:** Passengers can book trips.
- **Payments:** Secure trip payments.

### 🔹 Trips
- View available trips with **departure & endpoint, price, time, and duration**.

### 🔹 Reviews System
- Both **passengers and drivers** can review each other.
- Users can see the **total number of reviews & average rating**.

## 🏗 Tech Stack
- **Backend:** Python, FastAPI
- **Authentication:** OAuth2, JWT
- **Architecture:** MVC
- **Database:** _[sqllite]_

## 🚀 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/trip-share-app.git
   cd car-sharing
   pip install -r requirements.txt
   uvicorn main:app --reload to run the app on your browser
