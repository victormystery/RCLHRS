# Regent College London HR Reporting System (RCLHRS)

A FastAPI-based RESTful API for managing HR operations at Regent College London. This system provides CRUD functionality for employees, DBS checks, Home Office requests, and Bank requests, with user authentication, role-based access control, and PostgreSQL database integration.

## Features

- Employee management (CRUD)
- DBS, Home Office, and Bank request management
- User registration and login
- Role-based access control (Admin, HR)
- JWT authentication
- PostgreSQL database (via SQLAlchemy)
- Pydantic v2 support
- .env configuration for virtual environment

## Project Structure

```
├── main.py 
├── model.py
├── schemas.py
├── database.py
├── routers/
│   ├── users.py
│   ├── employees.py
│   ├── bank_request.py
│   ├── home_office.py
│   └── dbs.py
├── auth/
│   ├── auth.py
│   └── dependencies.py
├── .env
├── requirements.txt
└── README.md

```

## Setup Instructions

1. **Clone the repository**
   ```powershell
   git clone https://github.com/victormystery/RCLHRS.git
   cd RCLHRS
   ```
2. **Checkout to a new branch**
   ```powershell
   git checkout -b <your-feature-branch>
   ```
3. **Create and activate a virtual environment**
   ```powershell
   python -m venv .env
   ```

   ```powershell
   .env\Scripts\activate
   ```   
4. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
5. **Configure your `.env` file**
   - Add the `DATABASE_URL` and `SECRET_KEY`.
6. **Run the application**
   ```powershell
   uvicorn main:app --reload
   ```

## API Usage

- Access the interactive docs at: `http://127.0.0.1:8000/docs`
- Use the `/users/register` and `/users/login` endpoints for authentication.
- Use the `/employees`, `/bank_requests`, `/home_office_requests`, and `/dbs_checks` endpoints for resource management.

## License

This project is for educational use at Regent College London.
