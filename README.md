# QuickDesk: A Flask-Based Helpdesk Application

QuickDesk is a robust and user-friendly helpdesk application built with Flask, SQLAlchemy, and Bootstrap. It provides a streamlined platform for users to submit support tickets, for support agents to manage and resolve issues, and for administrators to oversee the entire system.
<img width="1902" height="907" alt="Landing" src="https://github.com/user-attachments/assets/4fdb8007-3cdc-4db3-a3c2-bb3f8fb1ab41" />


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
    <img width="691" height="911" alt="Registration" src="https://github.com/user-attachments/assets/ea555385-3eeb-4674-ba1d-87c96fb132a4" />


* **Log In:** Securely access your account.
* **User Dashboard:**
    * View all your submitted tickets in a professional, paginated list.
    * Filter tickets by status (e.g., "Show open only"), category, or specific status (Open, In Progress, Resolved, Closed).
    * Sort tickets by "Most Comments" or "Most Votes."
    * Search for tickets by subject or description.
    * See the number of conversations (comments) on each ticket.
    * Upvote or downvote tickets.
    * **Notifications:** Get notified by a bell icon in the navigation bar when an admin or agent replies to your ticket.
    <img width="1876" height="898" alt="user_dashboard_1" src="https://github.com/user-attachments/assets/4012448d-2f77-4dac-adfd-a2cd1cd58a62" />
    <img width="1862" height="912" alt="user_dashboard_2" src="https://github.com/user-attachments/assets/30a94e67-70bc-45c3-b882-fae3df9c24f6" />
    <img width="1087" height="557" alt="user_dashboard_3" src="https://github.com/user-attachments/assets/885b0f5d-1434-43db-b323-5d54d45a6d50" />
    <img width="1102" height="900" alt="user_dashboard_4" src="https://github.com/user-attachments/assets/19556833-dc27-49b7-b4ac-14e56f99de07" />





* **Ask a Question (Create a Ticket):**
    * Submit new support tickets with a clear subject and detailed description.
    * Select a relevant category for your ticket.
    * **File Attachments:** Attach up to 5 files (images, videos, PDFs, etc.) to your ticket.
    * **Professional Form Design:** A very professional and user-friendly form for submitting questions.
    <img width="1858" height="912" alt="Ask_queston" src="https://github.com/user-attachments/assets/0defd4b2-99d6-4cde-ad75-b683c3b747cf" />



* **View Ticket Details:**
    * Access a dedicated page for each ticket to view its full description.
    * See all associated attachments with download links.
    * Read through all comments, including who posted them (user, agent, or admin) and when.
    * Add new comments to the ticket.
    <img width="721" height="905" alt="user_view" src="https://github.com/user-attachments/assets/7ca84630-17a6-4d38-b663-262695acadc0" />



* **Profile Management:**
    * View and edit your personal details (name, mobile number, gender).
    * Update your residential address, education details, and occupation details.
    * **Request Agent Upgrade:** End users can request to be promoted to a "Support Agent" role, which an administrator can then approve or reject.
    <img width="1845" height="912" alt="profile" src="https://github.com/user-attachments/assets/ecdf1d28-64f7-40ff-b89f-c4e2851cf018" />


### Support Agent

As a Support Agent, you can:

* **Log In:** Access your agent dashboard.
* **Agent Dashboard:**
    * Get an overview of total tickets, assigned tickets, and unassigned tickets.
    * **Ticket Status Analytics:** View a doughnut chart showing the distribution of tickets by their status (Open, In Progress, Resolved, Closed).
    * View a comprehensive list of all tickets.
    * Filter tickets by status and search by subject/description.
    <img width="750" height="906" alt="Agent_Dashboard" src="https://github.com/user-attachments/assets/fbdc739d-3ef9-4c4a-809b-31fa13603360" />


* **View Ticket Details:**
    * Access the same detailed ticket view as end-users.
    * **Agent Actions:** Change the status of a ticket (Open, In Progress, Resolved, Closed).
    * Assign unassigned tickets to yourself.
    * Add comments to tickets, which will notify the original ticket author.
    <img width="762" height="896" alt="Agent_view" src="https://github.com/user-attachments/assets/4800ca7e-d827-46b9-bc13-8bae256d7245" />



### Admin

As an Admin, you have full control over the application:

* **Log In:** Access the admin dashboard.
* **Admin Dashboard:**
    * See a high-level overview of total tickets, total users, and pending upgrade requests.
    * **Ticket Analytics:** View charts showing ticket distribution by status and by category.
    * Access quick links to "Manage Categories" and "Manage Users."
    * View a list of all tickets in the system.
    <img width="717" height="906" alt="Admin_Dashboard" src="https://github.com/user-attachments/assets/0c082b07-a86d-434f-8075-b39cc3a91d4e" />


* **User Management:**
    * View a list of all registered users.
    * Change the role of any user (End User, Support Agent, Admin) directly from the table.
    * **Professional Interface:** A clean and intuitive table for managing user roles.
    <img width="1328" height="898" alt="User_Management" src="https://github.com/user-attachments/assets/4cdd314a-4560-4a3d-aa93-c17ba24976d9" />


* **Category Management:**
    * View all existing ticket categories.
    * Add new categories to help classify tickets more effectively.
    * See how many tickets are associated with each category.
    * **Professional Interface:** A dedicated page for managing categories.
    <img width="1300" height="900" alt="Category_Management" src="https://github.com/user-attachments/assets/836845e7-acfd-4f3c-9b92-3fbd9b5d886c" />


* **Manage Upgrade Requests:**
    * Review and either accept or reject requests from end-users to become support agents.
    <img width="1063" height="832" alt="request" src="https://github.com/user-attachments/assets/2950e068-9a69-4870-9056-b1d9cad30fe3" />


---

## 2. Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x** (recommended Python 3.8+)
* **pip** (Python package installer, usually comes with Python)

### Installation

1.  **Clone the repository (or download the project files):**
    ```bash
    git clone https://github.com/Shaik-Althaf-Techazsure/Quick_Task_Odoo
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
<img width="691" height="911" alt="Registration" src="https://github.com/user-attachments/assets/1a745b0f-7f47-4e60-9060-1779bde26067" />

### User Dashboard
<img width="1876" height="898" alt="user_dashboard_1" src="https://github.com/user-attachments/assets/a75feb6b-dce2-4f69-92e5-c6ef04fc863f" />
<img width="1862" height="912" alt="user_dashboard_2" src="https://github.com/user-attachments/assets/8e4792d8-ce40-424b-9fe4-58078d73e9fe" />
<img width="1087" height="557" alt="user_dashboard_3" src="https://github.com/user-attachments/assets/b53f90e0-9a9c-4e1e-b576-14f4b74b8175" />
<img width="1102" height="900" alt="user_dashboard_4" src="https://github.com/user-attachments/assets/56d79105-6c56-45fe-8fb6-dfa35576f755" />




### Ask a Question Page
<img width="1858" height="912" alt="Ask_queston" src="https://github.com/user-attachments/assets/31a46609-1aa7-4a65-ad8a-9752c98f810b" />


### Profile Page
<img width="1845" height="912" alt="profile" src="https://github.com/user-attachments/assets/d9b2a117-d58d-41ce-b417-35e520d28b66" />


### Admin Dashboard
<img width="717" height="906" alt="Admin_Dashboard" src="https://github.com/user-attachments/assets/d0c30fc1-ebfa-4125-83e8-b05c3ea6a187" />


### Agent Dashboard
<img width="750" height="906" alt="Agent_Dashboard" src="https://github.com/user-attachments/assets/827b384f-b40e-4763-882c-a326c1820118" />


### Ticket Details Page
<img width="1210" height="898" alt="Ticket details" src="https://github.com/user-attachments/assets/514aeae6-07d2-47b8-84f5-ad5da760f21f" />


### User Management Page
<img width="1328" height="898" alt="User_Management" src="https://github.com/user-attachments/assets/581830fa-204e-470b-9ad7-44f0cb0553f8" />


### Category Management Page
<img width="1300" height="900" alt="Category_Management" src="https://github.com/user-attachments/assets/69456a19-b075-4bf7-821e-68a1d157bfd7" />

