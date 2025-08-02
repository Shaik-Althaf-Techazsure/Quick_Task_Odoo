# QuickDesk: A Flask-Based Helpdesk Application

QuickDesk is a robust and user-friendly helpdesk application built with Flask, SQLAlchemy, and Bootstrap. It provides a streamlined platform for users to submit support tickets, for support agents to manage and resolve issues, and for administrators to oversee the entire system.

## Table of Contents

1.  [Features by Role](#features-by-role)
    * [End User](#end-user)
    * [Support Agent](#support-agent)
    * [Admin](#admin)
2.  [Setup Instructions](#setup-instructions)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Database Initialization/Migration](#database-initializationmigration)
    * [Running the Application](#running-the-application)
    * [Email Configuration (Important for OTP)](#email-configuration-important-for-otp)
3.  [Screenshots](#screenshots)

---

## 1. Features by Role

### End User

As an End User, you can:

* **Register a New Account:**
    * Create a new user account with a unique username, name, email, mobile number, and gender.
    * Upload a profile picture during registration.
    * **Email OTP Verification:** Your email is verified using a One-Time Password (OTP) sent to your provided email address (or printed to the console for debugging).
    * **Professional Registration Widget:** A clean and modern registration form.
    ![Registration Page Screenshot Placeholder]

* **Log In:** Securely access your account.
* **User Dashboard:**
    * View all your submitted tickets in a professional, paginated list.
    * Filter tickets by status (e.g., "Show open only"), category, or specific status (Open, In Progress, Resolved, Closed).
    * Sort tickets by "Most Comments" or "Most Votes."
    * Search for tickets by subject or description.
    * See the number of conversations (comments) on each ticket.
    * Upvote or downvote tickets.
    * **Notifications:** Get notified by a bell icon in the navigation bar when an admin or agent replies to your ticket.
    ![User Dashboard Screenshot Placeholder]

* **Ask a Question (Create a Ticket):**
    * Submit new support tickets with a clear subject and detailed description.
    * Select a relevant category for your ticket.
    * **File Attachments:** Attach up to 5 files (images, videos, PDFs, etc.) to your ticket.
    * **Professional Form Design:** A very professional and user-friendly form for submitting questions.
    ![Ask a Question Page Screenshot Placeholder]

* **View Ticket Details:**
    * Access a dedicated page for each ticket to view its full description.
    * See all associated attachments with download links.
    * Read through all comments, including who posted them (user, agent, or admin) and when.
    * Add new comments to the ticket.
    ![Ticket Details Page Screenshot Placeholder]

* **Profile Management:**
    * View and edit your personal details (name, mobile number, gender).
    * Update your residential address, education details, and occupation details.
    * **Request Agent Upgrade:** End users can request to be promoted to a "Support Agent" role, which an administrator can then approve or reject.
    ![Profile Page Screenshot Placeholder]

### Support Agent

As a Support Agent, you can:

* **Log In:** Access your agent dashboard.
* **Agent Dashboard:**
    * Get an overview of total tickets, assigned tickets, and unassigned tickets.
    * **Ticket Status Analytics:** View a doughnut chart showing the distribution of tickets by their status (Open, In Progress, Resolved, Closed).
    * View a comprehensive list of all tickets.
    * Filter tickets by status and search by subject/description.
    ![Agent Dashboard Screenshot Placeholder]

* **View Ticket Details:**
    * Access the same detailed ticket view as end-users.
    * **Agent Actions:** Change the status of a ticket (Open, In Progress, Resolved, Closed).
    * Assign unassigned tickets to yourself.
    * Add comments to tickets, which will notify the original ticket author.
    ![Ticket Details Page Screenshot Placeholder]

### Admin

As an Admin, you have full control over the application:

* **Log In:** Access the admin dashboard.
* **Admin Dashboard:**
    * See a high-level overview of total tickets, total users, and pending upgrade requests.
    * **Ticket Analytics:** View charts showing ticket distribution by status and by category.
    * Access quick links to "Manage Categories" and "Manage Users."
    * View a list of all tickets in the system.
    ![Admin Dashboard Screenshot Placeholder]

* **User Management:**
    * View a list of all registered users.
    * Change the role of any user (End User, Support Agent, Admin) directly from the table.
    * **Professional Interface:** A clean and intuitive table for managing user roles.
    ![User Management Page Screenshot Placeholder]

* **Category Management:**
    * View all existing ticket categories.
    * Add new categories to help classify tickets more effectively.
    * See how many tickets are associated with each category.
    * **Professional Interface:** A dedicated page for managing categories.
    ![Category Management Page Screenshot Placeholder]

* **Manage Upgrade Requests:**
    * Review and either accept or reject requests from end-users to become support agents.
    ![Admin Dashboard Screenshot Placeholder (showing pending requests section)]

---

## 2. Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x** (recommended Python 3.8+)
* **pip** (Python package installer, usually comes with Python)

### Installation

1.  **Clone the repository (or download the project files):**
    ```bash
    git clone <your-repository-url>
    cd quickdesk
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv virtual
    ```

3.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\virtual\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source virtual/bin/activate
        ```

4.  **Install the required Python packages:**
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug Flask-Mail Flask-Paginate
    ```

### Database Initialization/Migration

This application uses SQLite, and the database schema is managed by SQLAlchemy. Whenever you add new columns or tables to your models (`app.py`), you need to re-initialize the database.

1.  **Delete the existing database file:**
    ```bash
    # Ensure your Flask server is NOT running
    del quickdesk.db  # On Windows
    # rm quickdesk.db   # On macOS/Linux
    ```
    **Warning:** This will delete all existing user data, tickets, and categories.

2.  The database will be automatically created with the latest schema when you run `app.py`.

### Running the Application

1.  **Ensure your virtual environment is active.**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Email Configuration (Important for OTP)

The application uses Flask-Mail for sending OTPs during registration.

1.  **Set up a Gmail App Password:**
    * Go to your Google Account security settings: [https://myaccount.google.com/security](https://myaccount.google.com/security)
    * Enable **2-Step Verification** if it's not already enabled.
    * Under "Signing in to Google," click on **"App passwords."**
    * Generate a new App password for "Mail" and "Windows Computer" (or "Other" if on Linux/macOS).
    * **Copy the 16-character password.**

2.  **Update `app.py`:**
    Replace the placeholders in `app.config` with your Gmail address and the generated App Password:

    ```python
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Your Gmail address
    app.config['MAIL_PASSWORD'] = 'your_generated_16_digit_app_password' # Use the App Password here
    ```

3.  **Troubleshooting Email Sending:**
    * If you encounter `WinError 10060` or emails are not arriving, check your firewall/antivirus, ensure 2-Step Verification is active, and try generating a new App Password.
    * **Debugging Fallback:** If email sending continues to fail, the `send_otp` function in `app.py` is configured to print the OTP directly to your Flask server's console for testing purposes. Look for `--- DEBUG: OTP for ...` in your terminal.

---

## 3. Screenshots

*(Replace these placeholders with actual screenshots of your running application)*

### Registration Page
![Screenshot of Registration Page]

### User Dashboard
![Screenshot of User Dashboard]

### Ask a Question Page
![Screenshot of Ask a Question Page]

### Profile Page
![Screenshot of Profile Page]

### Admin Dashboard
![Screenshot of Admin Dashboard]

### Agent Dashboard
![Screenshot of Agent Dashboard]

### Ticket Details Page
![Screenshot of Ticket Details Page]

### User Management Page
![Screenshot of User Management Page]

### Category Management Page
![Screenshot of Category Management Page]
