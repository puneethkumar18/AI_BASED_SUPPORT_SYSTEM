# AI-Based Support System

An AI-powered IT Support Ticket Management System built using **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, **Docker**, and **AWS**. The system enables users to create support tickets, automatically categorizes them using **Google Gemini AI**, and provides a complete ticket lifecycle with authentication, role-based access control, comments, attachments, history tracking, caching, background email notifications, and cloud deployment.

---

## Features

### Authentication & Authorization
- JWT Authentication
- User Registration & Login
- Password Hashing (bcrypt)
- Role-Based Access Control (RBAC)
- Protected API Endpoints

### Ticket Management
- Create Ticket
- Update Ticket
- Delete Ticket
- View All Tickets
- View My Tickets
- Assign Ticket to Support Agent
- Change Ticket Status
- Ticket Priority
- Ticket Category
- AI Generated Summary
- Suggested Resolution

### AI Integration (Google Gemini)
- Automatic Ticket Categorization
- Automatic Priority Prediction
- Ticket Summarization
- Suggested Resolution Generation

### Ticket History
- Track Ticket Creation
- Track Status Changes
- Track Assignment Changes

### Comments
- Add Comments
- View Ticket Comments

### Attachments
- Upload Attachments
- Download Attachments

### Dashboard
- Ticket Statistics
- Status Summary
- Cached Dashboard Responses using Redis

### Email Notifications
- Ticket Created Email
- Ticket Assigned Email
- Ticket Status Update Email
- Background Processing using Celery

### Background Processing
- Celery
- Redis Broker
- Asynchronous Email Tasks

### Database
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations

### Deployment
- Docker
- Docker Compose
- AWS EC2
- Amazon RDS PostgreSQL

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Authentication | JWT |
| Password Hashing | Passlib (bcrypt) |
| Validation | Pydantic |
| AI | Google Gemini |
| Background Tasks | Celery |
| Cache | Redis |
| Containerization | Docker |
| Deployment | AWS EC2 |
| Managed Database | Amazon RDS |
| API Documentation | Swagger UI |

---

# Project Architecture

```
                    +----------------------+
                    |      Client          |
                    +----------+-----------+
                               |
                               |
                        HTTP REST API
                               |
                               ▼
                    +----------------------+
                    |      FastAPI         |
                    +----------+-----------+
                               |
          +--------------------+---------------------+
          |                    |                     |
          ▼                    ▼                     ▼
 Authentication          Ticket Service        AI Service
                               |                     |
                               |                     ▼
                               |              Google Gemini
                               |
        +----------------------+-------------------+
        |                      |                   |
        ▼                      ▼                   ▼
 PostgreSQL (RDS)         Redis Cache        Celery Worker
        |                                          |
        |                                          ▼
        ▼                                    Email Service

```

---

# Project Structure

```
AI_BASED_SUPPORT_SYSTEM
│
├── alembic/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── middleware/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── uploads/
│   └── main.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Implemented Modules

## Authentication
- User Registration
- Login
- JWT Token Generation
- Password Encryption
- Current User API

---

## Role Based Access

### Admin
- View all tickets
- Assign tickets
- Manage users
- Change ticket status

### Support Agent
- View assigned tickets
- Update tickets
- Add comments
- Resolve issues

### User
- Create ticket
- View own tickets
- Upload attachments
- View ticket history

---

# Ticket Workflow

```
User Creates Ticket
        │
        ▼
Gemini AI
(Category, Priority,
Summary,
Suggested Resolution)
        │
        ▼
Ticket Stored
        │
        ▼
Email Sent
        │
        ▼
Admin Assigns Ticket
        │
        ▼
Support Agent
        │
        ▼
Comment
        │
        ▼
Status Update
        │
        ▼
History Logged
```

---

# AI Workflow

```
Ticket Title
        +
Ticket Description
        │
        ▼
Google Gemini API
        │
        ▼
Returns

• Category

• Priority

• Summary

• Suggested Resolution
        │
        ▼
Stored in Database
```

---

# Redis Caching

Currently Cached

- Dashboard Summary

Future Scope

- Frequently Accessed Tickets
- User Session Data

---

# Background Jobs

Celery is used for

- Ticket Created Email
- Ticket Assignment Email
- Status Change Email

Broker

```
Redis
```

---

# Database Tables

- users
- tickets
- comments
- attachments
- ticket_history
- alembic_version

---

# REST APIs

## Authentication

```
POST /register
POST /login
GET  /me
```

---

## Tickets

```
POST   /tickets
GET    /tickets
GET    /tickets/{id}
PUT    /tickets/{id}
DELETE /tickets/{id}
```

---

## Ticket Assignment

```
PUT /tickets/{id}/assign
```

---

## Ticket Status

```
PUT /tickets/{id}/status
```

---

## Comments

```
POST /comments
GET  /comments/{ticket_id}
```

---

## Attachments

```
POST /attachments/upload
GET  /attachments/{filename}
```

---

## Dashboard

```
GET /dashboard/summary
```

---

# Environment Variables

Create a `.env` file

```env
DATABASE_URL=postgresql://username:password@host:5432/ai_support_system

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your_email

MAIL_PASSWORD=your_password

MAIL_FROM=your_email

MAIL_SERVER=smtp.gmail.com

MAIL_PORT=587

REDIS_HOST=redis

REDIS_PORT=6379

REDIS_URL=redis://redis:6379/0

CELERY_BROKER=redis://redis:6379/0

CELERY_BACKEND=redis://redis:6379/0

GEMINI_API_KEY=your_api_key
```

---

# Local Setup

Clone repository

```bash
git clone https://github.com/yourusername/AI_BASED_SUPPORT_SYSTEM.git

cd AI_BASED_SUPPORT_SYSTEM
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Alembic

```bash
alembic upgrade head
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

---

# Docker Deployment

```bash
docker compose up --build
```

---

# AWS Deployment

- Amazon EC2
- Amazon RDS PostgreSQL
- Docker
- Docker Compose

Deployment Steps

1. Launch EC2
2. Create RDS PostgreSQL
3. Configure Security Groups
4. Clone Repository
5. Configure `.env`
6. Build Docker Containers
7. Run Alembic
8. Access FastAPI

---

# Security Features

- JWT Authentication
- Password Hashing
- Role-Based Authorization
- Environment Variables
- Protected APIs

---

# Future Improvements

- Amazon S3 for File Storage
- Nginx Reverse Proxy
- HTTPS with Let's Encrypt
- CI/CD using GitHub Actions
- Monitoring with CloudWatch
- Rate Limiting
- API Versioning
- Audit Logs

---

# Author

**Puneeth Kumar**

Backend Software Engineer

**Tech Stack**

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Redis
- Celery
- AWS
- Google Gemini AI

---

# License

This project is licensed under the MIT License.
