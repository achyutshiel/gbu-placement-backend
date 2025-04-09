# 🎓 GBU Placement Portal (Backend)

This is the **Django REST API backend** for the Gautam Buddha University Placement Portal. It supports student/admin registration, JWT-based login, resume/marksheet upload, job applications, skill-matching, email notifications, and admin tracking of placement status.

---

## 📦 Tech Stack

- Python 3.12
- Django 5.0+
- Django REST Framework 3.14+
- SimpleJWT for authentication
- SQLite3 for local development
- Postman for API testing

### 🔧 Dependencies (in requirements.txt)
```
Django>=5.0
djangorestframework>=3.14
djangorestframework-simplejwt>=5.2.2
```

---

## ⚙️ Setup Guide

```bash
# 1. Clone the project
git clone https://github.com/achyutshiel/gbu-placement-backend.git
cd gbu-placement-backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## 🔐 Authentication with JWT

- Login: `POST /api/token/`
- Use `access` token in headers:
```
Authorization: Bearer <access_token>
```

---

## 📬 API Endpoints

| Endpoint                           | Method | Description                                |
|------------------------------------|--------|--------------------------------------------|
| `/api/register/student/`           | POST   | Register new student                       |
| `/api/register/admin/`             | POST   | Register new admin                         |
| `/api/token/`                      | POST   | Login and receive JWT token                |
| `/api/apply/`                      | POST   | Student applies for a company              |
| `/api/mark-placed/<student_id>/`   | POST   | Admin marks student as placed              |
| `/api/match-skills/<student_id>/`  | GET    | Check skill match, send email if matched   |
| `/admin/`                          | GET    | Django admin panel                         |

---

## 🧪 Testing in Postman

### Student Registration
```
POST /api/register/student/
Content-Type: application/json
{
  "username": "student123",
  "email": "student@example.com",
  "password": "studentpass",
  "branch": "CSE",
  "skills": "Python, SQL",
  "resume": "<file>",
  "marksheet": "<file>"
}
```

### Admin Registration
```
POST /api/register/admin/
{
  "username": "admin1",
  "email": "admin@example.com",
  "password": "adminpass",
  "role": "Training"
}
```

### Login (JWT Token)
```
POST /api/token/
{
  "username": "admin1",
  "password": "adminpass"
}
```
![image](https://github.com/user-attachments/assets/83f96f23-dad7-46cd-82e7-a8edd18c0b8d)


Use returned `access` token for headers:
```
Authorization: Bearer <access_token>
```

---

## 📧 Email Notifications

- Sent when:
  - Student skills match a company
  - Admin marks student as placed
- Emails are printed to terminal (`console backend`):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 👨‍💼 Author

- 💡 Developed by: [Achyut Shiel](https://github.com/achyutshiel)

---

## 📌 Final Notes

- All features implemented and tested via Postman
- Code pushed fully, including `venv/` and DB for submission
- Submission-ready — run, test, and deploy easily

---

**Good luck, and happy placement! 🚀**
