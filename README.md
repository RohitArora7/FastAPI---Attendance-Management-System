ASM

Attendance Management System (FastAPI)
A lightweight and scalable backend for managing attendance, built using FastAPI, SQLAlchemy, and JWT authentication.

Clone the Project
```
git clone https://github.com/your-username/attendance-management-system.git
cd attendance-management-system
```

Create and Activate Virtual Environment
```python3 -m venv attendance
source attendance/bin/activate```

Install Dependencies
# FastAPI and Uvicorn
```pip install "fastapi[standard]"
pip install "uvicorn[standard]"

# Core Dependencies
pip install sqlalchemy pydantic

# Authentication
pip install email-validator
pip install python-jose[cryptography] passlib[bcrypt]
pip install python-multipart```
 
OR

```pip install -r requirements.txt```

Run the Server
```uvicorn main:app --reload ```


FEATURES

User Authentication (JWT)
User Registration
User Records
Secure APIs with token-based access

