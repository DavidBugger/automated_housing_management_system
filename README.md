# House Listing Management System

This project is a Django application for managing house listings. Users can add, view, update, and delete house listings with features like location, price, and number of rooms. The application also allows users to upload images of the houses.

## Features

- Add new house listings with details like location, price, and number of rooms.
- Upload images of the houses.
- View all house listings in a list or detailed view.
- Update existing house listings.
- Delete house listings.

## Prerequisites

- Python 3.8+
- Django 3.2+
- pandas (if needed for data manipulation)
- pillow for image handling
- jQuery (for frontend form submission)

## Setup and Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/house-listing-management.git
    cd house-listing-management
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

1. **Access the main page:** Navigate to `http://127.0.0.1:8000/` to see the main page.

2. **Manage house listings:**
    - Go to `http://127.0.0.1:8000/main/` to view all house listings.
3. **Authentication**
To register into the system you can navigate to http://127.0.0.1:8000/sign-up/
4. **Login as an Admin**
http://127.0.0.1:8000/admin/
username: globen
password: test@123!
