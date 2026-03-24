<div align="center">

# 📝 To Do 

### A production-ready built with FastAPI & PostgreSQL

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Docker](#-docker-setup)

</div>

---

## 📖 About

A fully-featured **Todo API** with user authentication, task management, pagination, and filtering. Built following best practices with clean, modular code and complete Swagger documentation.

> ✅ Every user can only access their own tasks — fully secured with JWT tokens.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **JWT Authentication** | Secure login with token-based auth |
| 👤 **User Management** | Register, login, view profile |
| ✅ **Task CRUD** | Create, read, update, delete tasks |
| 🔍 **Filter Tasks** | Filter by completed / pending status |
| 📄 **Pagination** | Page-based task listing |
| 🛡️ **Data Isolation** | Users can only access their own tasks |
| 📚 **Auto Docs** | Swagger UI + ReDoc out of the box |
| 🐳 **Docker Ready** | One-command deployment |
| 🗄️ **Migrations** | Alembic-based database migrations |

---

## 🛠 Tech Stack

```
Backend     →  FastAPI (Python)
Database    →  PostgreSQL
ORM         →  SQLAlchemy 2.0
Validation  →  Pydantic v2
Auth        →  JWT (python-jose) + bcrypt (passlib)
Migrations  →  Alembic
Server      →  Uvicorn (ASGI)
Container   →  Docker + Docker Compose
```

---

## 📁 Project Structure

```
todo-api/
├── app/
│   ├── main.py          # FastAPI app entry point & router registration
│   ├── database.py      # PostgreSQL connection (SQLAlchemy engine)
│   ├── models.py        # Database table models (User, Task)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # All database operations (CRUD)
│   ├── auth.py          # JWT token creation & password hashing
│   └── routes/
│       ├── user.py      # /register  /login  /me
│       └── task.py      # /tasks  CRUD endpoints
├── alembic/
│   ├── env.py           # Alembic migration config
│   └── versions/        # Auto-generated migration files
├── alembic.ini          # Alembic settings
├── .env                 # Environment variables (not committed)
├── .env.example         # Example env file
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
└── docker-compose.yml   # Multi-container setup (API + DB)
```

---

## 🚀 Quick Start

### Prerequisites

- [Python 3.10+](https://python.org/downloads/)
- [PostgreSQL](https://postgresql.org/download/)
- [Git](https://git-scm.com/)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/todo-api.git
cd todo-api
```

---

### Step 2 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Configure Environment

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tododb
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### Step 5 — Create Database

Open **pgAdmin** or **psql** and run:

```sql
CREATE DATABASE tododb;
```

---

### Step 6 — Run Migrations

```bash
alembic upgrade head
```

> **Note:** If you skip this step, tables are created automatically on server start via `Base.metadata.create_all()`.

---

### Step 7 — Start the Server

```bash
uvicorn app.main:app --reload
```

The server will start at:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | API Root |
| `http://127.0.0.1:8000/docs` | Swagger UI (Interactive Docs) |
| `http://127.0.0.1:8000/redoc` | ReDoc Documentation |

---

## 🐳 Docker Setup

No PostgreSQL installation needed — Docker handles everything.

### Start

```bash
docker-compose up --build
```

### Stop

```bash
docker-compose down
```

> API will be available at `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | ❌ | Register a new user |
| `POST` | `/login` | ❌ | Login and get JWT token |
| `GET` | `/me` | ✅ | Get current user profile |

### Tasks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/tasks/` | ✅ | List all tasks (filter + paginate) |
| `POST` | `/tasks/` | ✅ | Create a new task |
| `PUT` | `/tasks/{id}` | ✅ | Update a task |
| `DELETE` | `/tasks/{id}` | ✅ | Delete a task |

#### Query Parameters for `GET /tasks/`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `completed` | boolean | null | Filter: `true` or `false` |
| `page` | integer | 1 | Page number |
| `page_size` | integer | 10 | Results per page (max 100) |

---

## 🔧 Example Requests

### Register

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false}'
```

### Get All Tasks (with filter)

```bash
# All tasks
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Only pending tasks
curl "http://localhost:8000/tasks/?completed=false" \
  -H "Authorization: Bearer YOUR_TOKEN"

# With pagination
curl "http://localhost:8000/tasks/?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🗄️ Database Schema

### `users` table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Auto-increment primary key |
| `username` | VARCHAR(50) | Unique username |
| `email` | VARCHAR(100) | Unique email address |
| `hashed_password` | VARCHAR(255) | Bcrypt hashed password |
| `created_at` | TIMESTAMP | Auto-set on creation |

### `tasks` table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Auto-increment primary key |
| `title` | VARCHAR(200) | Task title (required) |
| `description` | TEXT | Task details (optional) |
| `completed` | BOOLEAN | Default: `false` |
| `created_at` | TIMESTAMP | Auto-set on creation |
| `updated_at` | TIMESTAMP | Auto-updated on change |
| `user_id` | INTEGER (FK) | References `users.id` |

---

## 🔒 Security

- Passwords are hashed using **bcrypt** — never stored as plain text
- All task routes are protected with **JWT Bearer tokens**
- Each user can **only access their own tasks** — cross-user access returns `404`
- Tokens expire after **30 minutes** (configurable in `.env`)

---

## 🧪 Running Tests with Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Open `http://127.0.0.1:8000/docs`
3. Register a user via `POST /register`
4. Login via `POST /login` — copy the `access_token`
5. Click **Authorize 🔒** → paste the token → **Authorize**
6. All protected endpoints are now accessible

---

## 🌱 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | — |
| `SECRET_KEY` | JWT signing secret | — |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `30` |

---

## 📦 Dependencies

```
fastapi              # Web framework
uvicorn[standard]    # ASGI server
sqlalchemy           # ORM
psycopg2-binary      # PostgreSQL driver
alembic              # Database migrations
pydantic[email]      # Data validation
pydantic-settings    # Settings management
python-jose          # JWT tokens
passlib[bcrypt]      # Password hashing
python-multipart     # Form data support
python-dotenv        # Environment variables
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

<div align="center">

Made with ❤️ using **FastAPI** + **PostgreSQL**

⭐ **Star this repo if you found it helpful!**

</div>
