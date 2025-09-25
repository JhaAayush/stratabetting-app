# Stratabetting - Kritansh Betting Platform

This is a Flask-based web application for managing a virtual betting system for the Kritansh sports event at IIM Amritsar. It features a sleek, modern dark-mode interface with a theme switcher and robust admin controls.

---

## Features

-   **User Authentication**: Students can register and log in using their roll numbers and full names.
-   **Password Management**: Users can securely change their passwords after logging in.
-   **Virtual Currency**: Each student starts with 200 points to place bets.
-   **Dynamic Betting Markets**: Admins can create events (e.g., Cricket) and add multiple betting questions with different options and odds.
-   **Elegant Admin Panel**: A secure area for admins to:
    -   Create, activate, deactivate, and **delete** sports events.
    -   Add, edit, and close betting questions.
    -   Update team squads.
    -   Declare winning results, which automatically calculates and distributes points.
-   **Advanced Excel Exports**:
    -   Download a detailed report of all bets, pivoted by user for each event.
    -   Download a sorted leaderboard of all participants who have placed at least one bet.
-   **Modern UI/UX**:
    -   A beautiful dark-mode-first design.
    -   A theme switcher to toggle between dark and light modes, with the user's preference saved.
    -   Password visibility toggles for improved usability.

---

## Tech Stack

-   **Backend**: Flask
-   **Database**: SQLite (via Flask-SQLAlchemy)
-   **Frontend**: HTML, Tailwind CSS
-   **Interactivity**: Alpine.js (for theme switching)
-   **Security**: Password hashing with Flask-Bcrypt
-   **Excel Export**: OpenPyXL

---

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/stratabetting-app.git](https://github.com/YourUsername/stratabetting-app.git)
    cd stratabetting-app
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    py -m venv venv
    venv\Scripts\activate

    # Install packages
    pip install -r requirements.txt
    ```

3.  **Initialize the Database:**
    This is a one-time command to create the `stratabet.db` file, set up all the tables, and create a default admin user.

    ```bash
    flask init-db
    ```
    This creates an admin user with:
    -   **Roll Number**: `admin`
    -   **Password**: `password`
    
4.  **Run the Application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## How to Use

-   **Students**: Go to the homepage, click "Register" to create an account. Then log in to access the dashboard, view events, and place bets.
-   **Admins**: Log in with the admin credentials. You will be redirected to the admin panel where you can manage the entire event.