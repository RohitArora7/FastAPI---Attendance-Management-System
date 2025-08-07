ASM

Attendance Management System (FastAPI)
Built using FastAPI, SQLAlchemy, and JWT authentication.

Clone the Project
```
git clone project
cd FastAPI---Attendance-Management-System
```

Create and Activate Virtual Environment
```
python3 -m venv attendance
source attendance/bin/activate
```

Install Dependencies
```
# FastAPI and Uvicorn
pip install "fastapi[standard]"
pip install "uvicorn[standard]"

# Core Dependencies
pip install sqlalchemy pydantic

# Authentication
pip install email-validator
pip install python-jose[cryptography] passlib[bcrypt]
pip install python-multipart
```
OR
```
pip install -r requirements.txt
```

Run the Server
```
uvicorn main:app --reload
```


FEATURES

User Authentication (JWT)
User Registration
User Records
Secure APIs with token-based access



USER REGISTGRATION
<img width="1739" height="526" alt="Register" src="https://github.com/user-attachments/assets/5ea51864-fdcc-46d4-8a26-1852875b5a91" />

ACCESS TOKEN
<img width="1739" height="526" alt="Access_token" src="https://github.com/user-attachments/assets/f32b9153-1959-45d8-88df-0ece1abc1de9" />

PROFILE LOGIN
<img width="1739" height="526" alt="Profile_login'" src="https://github.com/user-attachments/assets/3538bb7b-6a40-4c69-beec-d8c3cba854ba" />

