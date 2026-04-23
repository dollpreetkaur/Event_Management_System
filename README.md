# Event Management System

## Overview

This project is a simple **Event Management System** built using **Streamlit**.
It allows users to manage memberships with role-based access (Admin & User).

The application includes modules for:

* Membership Management
* Transactions (Add / Update Membership)
* Reports
* Admin Maintenance

---

## Live Application

 https://eventmanagementsystem-fqzahoqsptrzfzapfe9hzu.streamlit.app/

---

##  Technologies Used

* Python
* Streamlit
* SQLite (for deployment)
* MS SQL Server (used during local development)
* Pandas

---

##  Features

### Login System

* Secure login with username & password
* Role-based access:

  * **Admin** - Full access (Maintenance + Reports + Transactions)
  * **User**- Limited access (Transactions + Reports)

---

###  Add Membership

* Input: Name, Email, Duration
* Duration options:

  * 6 months (default)
  * 1 year
  * 2 years
* Email validation applied
* Auto-generated Membership ID
* Start date auto-filled

---

###Update Membership

* Fetch member using Membership ID
* Actions:

  * Extend membership (+6 months)
  * Cancel membership

---

###  Reports

* View all membership records
* Displays:

  * Membership ID
  * Name
  * Email
  * Duration
  * Status

---

###  Admin Maintenance

* View all members
* Delete member records
* Access restricted to Admin only

---

##  Validation Implemented

* Mandatory fields check
* Email format validation
* Numeric validation for Membership ID

---
##  Test Credentials

Admin:
* Username: `admin`
* Password: `admin123`

User:
* Username: `user1`
* Password: `user123`

---
## How to Run Locally
1. Clone the repository:

```bash
git clone https://github.com/your-username/event-management-app.git
cd event-management-app
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Run the app:

```bash
streamlit run app.py
```
---

## Notes
* MS SQL Server was used during development.
* SQLite is used in deployment due to cloud compatibility.

---
##Future Improvements

* Search & filter functionality
* Export reports to Excel
* UI enhancements
* Event booking module

---

## 👨‍💻 Author

Developed as part of a technical assignment/project.

---
