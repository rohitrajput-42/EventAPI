# Event Management System

## Overview
This project is a Django REST API for managing events and ticket sales. The system allows users to register, create events (admin only), and purchase tickets for events.

## Features
- User registration with roles (Admin, User)
- JWT-based authentication
- Event creation and listing
- Ticket purchase with validation
- Custom SQL query for fetching event details

## Requirements
- Python 3.10
- Django 5.0.2
- Django REST Framework 3.15.2
- PostgreSQL
- Django REST Framework SimpleJWT

## Setup Instructions
### 1. Clone The Repository
You can simply clone the repo by the web url given in the repo on github

### 2. Create a virtual environment
python -m venv venv 
source venv/bin/activate # For Linux/Mac 
venv\Scripts\activate # For Windows

### 3. Install the Dependencies
pip install -r requirements.txt

### 4. Configure your database(IN this case POstgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Use 'django.db.backends.mysql' for MySQL
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',  # Default port for PostgreSQL, use '3306' for MySQL
    }
}

### 5. Run the migration commands
python manage.py makemigrations
python manage.py migrate

### 6. Create a superuser
You can create a superuser by passing this command: "python manage.py createsuperuser", to access admin panel.

### 7. Run the server
python manage.py runserver

### 8. Custom query:
SELECT e.id AS event_id, e.name AS event_name, e.date AS event_date, e.total_tickets, e.tickets_sold, (e.total_tickets - e.tickets_sold) AS tickets_remaining FROM events_event e ORDER BY e.tickets_sold DESC LIMIT 3;