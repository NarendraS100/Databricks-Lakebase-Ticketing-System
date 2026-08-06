# 🎫 Lakebase Ticketing System

A Flask-based ticket management application built on **Databricks Apps** using **Databricks Lakebase (PostgreSQL)** as the backend database.

This project demonstrates how to build a transactional web application on Databricks with support for viewing, creating, and updating support tickets.

---

## 🚀 Features

- View all support tickets
- View complete ticket details
- View all messages associated with a ticket
- Create a new support ticket
- Add a message to an existing ticket
- Update a ticket's status
- Filter tickets by status (Open, In Progress, Resolved)

---

## 🛠 Technology Stack

- Databricks Apps
- Databricks Lakebase (PostgreSQL)
- Flask
- psycopg2
- SQLAlchemy
- HTML
- CSS
- Jinja2 Templates

---

## 📂 Project Structure

```
Lakebase-Ticketing-System
│
├── app.py
├── lakebase.py
├── app.yaml
├── requirements.txt
│
├── templates
│   ├── index.html
│   ├── ticket_details.html
│   ├── create_ticket.html
│   ├── add_message.html
│   └── update_status.html
│
└── README.md
```

---

## 🗄 Database Schema

### tickets

| Column | Type |
|---------|------|
| ticket_id | varchar(20) |
| title | text |
| status | varchar(10) |
| created_by | varchar(50) |
| created_at | timestamp |

---

### ticket_messages

| Column | Type |
|---------|------|
| message_id | varchar(20) |
| ticket_id | varchar(20) |
| message_text | text |
| author | varchar(50) |
| created_at | timestamp |

`ticket_messages.ticket_id` references `tickets.ticket_id`.

---

## 🔄 Application Flow

```
Home Page
    │
    ├── View Tickets
    │
    ├── Create Ticket
    │
    └── Click Ticket
            │
            ▼
      Ticket Details
            │
            ├── Add Message
            │
            └── Update Status
```

---

## 📋 CRUD Operations

### Read

- View all tickets
- View ticket details
- View ticket messages

### Create

- Create a support ticket
- Add messages to a ticket

### Update

- Update ticket status

---

## 📸 Screenshots

Add screenshots here after deployment.

### Home Page

```
docs/home.png
```

### Ticket Details

```
docs/ticket_details.png
```

### Create Ticket

```
docs/create_ticket.png
```

### Update Status

```
docs/update_status.png
```

---

## ⚙️ Running the Application

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Lakebase

Configure the Databricks secret containing the PostgreSQL connection URL.

### Run

```bash
python app.py
```

---

## 📌 Sample Features Demonstrated

- Flask Routing
- Databricks Apps
- Lakebase Connectivity
- PostgreSQL CRUD Operations
- HTML Templates
- Status-based Filtering

---

## 🎯 Learning Outcomes

This project demonstrates how to:

- Build a transactional web application using Databricks Apps
- Connect Flask applications to Lakebase
- Design relational database schemas
- Perform CRUD operations using psycopg2
- Implement one-to-many relationships
- Develop a simple ticket management system

---

## 👤 Author

**Narendra Singh**

Data Engineer | Databricks | Apache Spark | Python | SQL
