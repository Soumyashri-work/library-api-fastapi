
📚 Library API — FastAPI + SQLite
A beginner-friendly Library Management REST API built using FastAPI, SQLite, SQLAlchemy ORM, and Pydantic.
This project satisfies all requirements of the given hands-on assignment, including authentication middleware and data statistics.

🚀 Tech Stack
Framework: FastAPI

Server: Uvicorn

Database: SQLite (library.db)

ORM: SQLAlchemy

Validation: Pydantic

Authentication: Custom Basic Auth Middleware

📁 Project Structure
library_api/
│
├── main.py          # FastAPI app + routes
├── database.py      # DB engine & session
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic schemas
├── auth.py          # Authentication logic
├── requirements.txt
├── library.db       # SQLite DB (auto-created)
└── .gitignore

⚙️ Setup & Run Instructions
1️⃣ Create virtual environment (optional but recommended)
python -m venv venv
Activate:

Windows

venv\Scripts\activate
Mac/Linux

source venv/bin/activate
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the application
uvicorn main:app --reload
Server runs at:

http://127.0.0.1:8000
Swagger UI:

http://127.0.0.1:8000/docs
⚠️ Note: All routes are protected by authentication middleware.

🔐 Authentication
Type: Basic Authentication

Credentials:

Username: admin

Password: password

Example (curl):
curl.exe -u admin:password http://127.0.0.1:8000/books
If credentials are missing or invalid:

{
  "detail": "Unauthorized"
}
🗄️ Database Design
Entities
Author

id, name, bio

Category

id, name

Book

id, title, ISBN, publication_year

author_id → Author

category_id → Category

Relationships
One Author → Many Books

One Category → Many Books

🔁 API Endpoints
📘 Authors
POST /authors — create author

🗂️ Categories
POST /categories — create category

📚 Books
POST /books — create book

GET /books — list books (filters + limit)

GET /books/{id} — get book by ID

Filters supported:

author_id

category_id

year

limit

📊 Stats & Business Checks
Implemented as required in the assignment:

Requirement	Endpoint
How many books	/stats/book-count
Average publication year	/stats/average-year
Earliest & latest book for author	/stats/author-range/{author_id}
Does author have books	/stats/author-has-books/{author_id}
All endpoints return safe responses (no crashes when data is missing).

🛡️ Authentication Middleware (Task 4)
Runs for every request

Returns 401 Unauthorized if:

Header missing

Invalid credentials

Attaches authenticated user to:

request.state.user
Authentication logic is centralized in auth.py, making it easy to extend later to:

Token-based auth

JWT

OAuth

🧪 Testing
Recommended (Windows):
curl.exe -u admin:password http://127.0.0.1:8000/books
Swagger UI can be used, but headers must be manually provided.



🏁 Notes
This project was built step-by-step as a learning-focused implementation, emphasizing clarity, correctness, and extensibility.

📌 Author
Soumyashri Mukund Inamdar
Assignment: FastAPI + SQLite — Hands-On




