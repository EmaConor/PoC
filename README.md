# Secure Login PoC

A proof-of-concept web application that demonstrates industry-standard security practices for user authentication. Built with Flask, it showcases how to implement a production-ready login system with defense-in-depth.

[Leer en Espanol](README.es.md)

---

## About The Project

This project was developed as part of a cybersecurity learning exercise by Equipo SECURITY. Its purpose is to illustrate how common web vulnerabilities can be mitigated through secure coding practices, without relying on third-party authentication services.

Every layer -- from the database query to the HTTP response headers -- is intentionally hardened to serve as a reference implementation for secure Flask development.

---

## Security Features Demonstrated

| # | Control | Implementation |
|---|---------|---------------|
| 1 | SQL Injection prevention | ORM-based queries via SQLAlchemy (`User.query.filter_by()`) |
| 2 | Password hashing | Werkzeug `generate_password_hash` / `check_password_hash` (pbkdf2:sha256) |
| 3 | Input validation | Whitelist regex `^[a-zA-Z0-9_.]+$`, max length 50 |
| 4 | Rate limiting | Flask-Limiter (200 requests/day, 50/hour per IP) |
| 5 | Secure session cookies | `HttpOnly`, `Secure`, `SameSite=Lax` |
| 6 | Security HTTP headers | CSP, X-XSS-Protection, X-Frame-Options, HSTS |
| 7 | TLS termination | Nginx reverse proxy with HTTPS (self-signed certs for development) |
| 8 | Least privilege (Docker) | Non-root `appuser` in container |
| 9 | Access control | `@login_required` decorator on protected routes |
| 10 | No hardcoded secrets | `SECRET_KEY` sourced from environment variable |

---

## Built With

- **Flask 3.0** -- Web framework
- **Flask-SQLAlchemy 3.1** -- ORM and database management
- **Flask-Login 0.6** -- User session management
- **Flask-Limiter 3.7** -- Rate limiting
- **Werkzeug 3.0** -- Password hashing utilities
- **Gunicorn 22** -- Production WSGI server
- **Nginx** -- Reverse proxy with TLS termination
- **Docker / Docker Compose** -- Containerization and orchestration
- **SQLite** -- Database engine (development)

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose

### Installation

Follow these steps to run the application locally:

**1. Clone the repository**

```bash
git clone https://github.com/EmaConor/PoC.git
cd PoC
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

- Windows (PowerShell):
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- Linux / macOS:
  ```bash
  source venv/bin/activate
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Copy the example environment file and adjust the values:

```bash
cp .env.example .env
```

Open `.env` and configure the following variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Used for session signing and CSRF tokens. Generate a strong random key. | `change-this-to-a-random-secret-key` |
| `DATABASE_URL` | Database connection string. SQLite path for development, PostgreSQL/MySQL for production. | `sqlite:///app.db` |
| `FLASK_ENV` | Application environment. Set to `development` for debug mode or `production` for hardened settings. | `development` |

> For production, generate a secure `SECRET_KEY`:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

**5. Initialize the database**

This creates all tables and inserts test users:

```bash
python init_db.py
```

**6. Run the application**

```bash
python app.py
```

The server will start at **http://127.0.0.1:5000**.

---

### Running with Docker

For a production-like environment with Nginx and HTTPS:

```bash
docker-compose up --build -d
docker-compose exec web python init_db.py
```

This starts two containers:
- **web** -- Flask application behind Gunicorn on port 5000 (internal only)
- **nginx** -- Reverse proxy with TLS on ports 80 and 443

Access the application at **https://localhost**.

---

## Default Credentials

The seed script creates the following test users:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| ema | emaema | user |
| yuri | yuri123 | user |
| gene | gene123 | user |

---

## API Endpoints

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/` | GET, POST | Login page. POST submits credentials for authentication. | No |
| `/dashboard` | GET | Protected dashboard showing logged-in user info. | Yes |
| `/logout` | GET | Terminates the session and redirects to login. | Yes |

---

## Project Structure

```
PoC/
├── app.py                 # Flask application entry point (routes, security headers, rate limiting)
├── config.py              # Configuration classes (Development, Production)
├── models.py              # SQLAlchemy User model with password hashing
├── init_db.py             # Database seeder (creates tables + test users)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
├── .env.example           # Environment variable template
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Docker Compose orchestration (Flask + Nginx)
├── nginx/
│   ├── nginx.conf         # Nginx configuration (HTTPS, reverse proxy)
│   └── certs/             # SSL certificates (self-signed for development)
├── templates/
│   ├── login.html         # Login form template
│   └── dashboard.html     # Dashboard template
└── instance/
    └── app.db             # SQLite database file (generated at runtime)
```

---

## Configuration

### Environment Variables

All runtime configuration is loaded from the `.env` file (see `.env.example`):

- **SECRET_KEY** -- Random string used for cryptographic signing. Required in production.
- **DATABASE_URL** -- Database URI. Defaults to `sqlite:///app.db`.
- **FLASK_ENV** -- Controls `development` vs `production` mode. In production mode, debug is disabled, testing is off, and CSRF protection is enabled.

### Configuration Classes

Defined in `config.py`:

| Setting | Development | Production |
|---------|-------------|------------|
| DEBUG | True | False |
| TESTING | True | False |
| WTF_CSRF_ENABLED | False | True |
| TEMPLATES_AUTO_RELOAD | True | False |
| SESSION_COOKIE_SECURE | True | True |
| SESSION_COOKIE_HTTPONLY | True | True |
| SESSION_COOKIE_SAMESITE | Lax | Lax |
| PERMANENT_SESSION_LIFETIME | 30 min | 30 min |
| REMEMBER_COOKIE_DURATION | 7 days | 7 days |

---

[Leer en Espanol](README.es.md)
