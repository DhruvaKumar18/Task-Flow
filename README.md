# Task Flow — Modern Django & PostgreSQL Task Management System

A full-featured, productivity-focused task management web application built with **Django 6** and **PostgreSQL**. **Task Flow** combines traditional to-do organization with an integrated focus timer, multi-session time tracking, categories, and an activity audit log.

---

## 🌟 Key Features

* **Task Management**: Create, edit, duplicate, delete, and filter tasks by status and priority.
* **Integrated Focus Timer**: Built-in stopwatch for every task supporting multiple **Start → Pause → Resume → Stop** sessions.
* **Accurate Time Tracking**: Session durations are tracked at the second level and automatically aggregated for total work time.
* **Category Organization**: Categorize tasks (e.g., *Work*, *Personal*, *Study*) with color-coded tags.
* **Audit Trail & Activity Log**: Automatic timestamped recording of every timer action (`START`, `PAUSE`, `RESUME`, `STOP`).
* **Due Date Tracking**: Dynamic indicators for *Overdue* and *Due Today* tasks.
* **User Authentication**: Secure user registration, login, logout, and user-isolated workspaces.
* **Responsive UI**: Clean, modern interface designed with Bootstrap 5 and Bootstrap Icons.

---

## 🏗️ Database Architecture

Task Flow uses a clean, relational 5-table database structure in **PostgreSQL**:

```
                       ┌──────────────────────┐
                       │       auth_user      │
                       │   (Account Owner)    │
                       └──────────┬───────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       ┌────────────────────┐          ┌────────────────────┐
       │   tasks_category   │          │     tasks_task     │
       │ (Folders & Labels) │◄─────────┤  (The Main Task)   │
       └────────────────────┘          └──────────┬─────────┘
                                                  │
                                  ┌───────────────┴───────────────┐
                                  ▼                               ▼
                       ┌────────────────────┐          ┌────────────────────┐
                       │ tasks_timesession  │          │ tasks_taskactivity │
                       │ (Stopwatch Laps)   │          │ (Action Audit Log) │
                       └────────────────────┘          └────────────────────┘
```

### Table Breakdown

1. **`auth_user`** (User): Django's built-in authentication model.
2. **`tasks_category`** (Category): Groups tasks into custom user-defined categories.
3. **`tasks_task`** (Task): The central task model holding title, description, priority, status, and due date.
4. **`tasks_timesession`** (TimeSession): Tracks individual focus sessions with `started_at`, `ended_at`, and `duration_seconds`.
5. **`tasks_taskactivity`** (TaskActivity): Historical log tracking actions (`START`, `PAUSE`, `RESUME`, `STOP`).

---

## 🛠️ Tech Stack

* **Backend**: Python 3.12, Django 6.1
* **Database**: PostgreSQL 18 (psycopg2)
* **Frontend**: HTML5, Vanilla JavaScript, CSS3, Bootstrap 5.3, Bootstrap Icons
* **Server**: Django WSGI Development Server

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* PostgreSQL installed and running locally
* Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/TaskFlow.git
   cd TaskFlow
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django psycopg2
   ```

4. **Configure PostgreSQL Database**:
   Create a database named `todo_db` in PostgreSQL:
   ```sql
   CREATE DATABASE todo_db;
   ```
   Ensure your database credentials in `config/settings.py` match your local PostgreSQL configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'todo_db',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional, for Django Admin)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📂 Project Structure

```
TodoProject/
│
├── accounts/               # User authentication (login, register, logout)
├── config/                 # Project settings, WSGI, URLs
├── tasks/                  # Core task management app
│   ├── models.py           # 5-table schema (Task, Category, TimeSession, TaskActivity)
│   ├── views.py            # Dashboard, timer controllers, CRUD operations
│   ├── forms.py            # Task forms with category integration
│   ├── admin.py            # Django admin registration
│   └── urls.py             # App route definitions
├── templates/              # HTML templates (Bootstrap 5)
│   ├── base.html           # Base layout and navbar
│   ├── dashboard.html      # Main task dashboard with live timers
│   ├── task_form.html      # Task creation and editing
│   ├── login.html          # Authentication login
│   └── register.html       # Account registration
├── static/                 # CSS and static assets
├── manage.py               # Django CLI utility
├── .gitignore              # Ignored files (venv, pycache)
└── README.md               # Project documentation
```