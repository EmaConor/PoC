# Secure Login PoC

Prueba de concepto de una aplicacion web de inicio de sesion segura, desarrollada con Flask. Este proyecto demuestra como implementar un sistema de autenticacion siguiendo las mejores practicas de seguridad informatica, aplicando defensa en profundidad en cada capa de la aplicacion.

[Read in English](README.md)

---

## Sobre el Proyecto

Este proyecto fue desarrollado como parte de un ejercicio de aprendizaje en ciberseguridad por Equipo SECURITY. Su objetivo es ilustrar como mitigar vulnerabilidades web comunes mediante practicas de codigo seguro, sin depender de servicios de autenticacion de terceros.

Cada capa de la aplicacion -- desde las consultas a la base de datos hasta las cabeceras HTTP de respuesta -- ha sido endurecida intencionalmente para servir como referencia de implementacion segura en Flask.

---

## Funcionalidades de Seguridad Demostradas

| # | Control | Implementacion |
|---|---------|---------------|
| 1 | Prevencion de inyeccion SQL | Consultas mediante ORM de SQLAlchemy (`User.query.filter_by()`) |
| 2 | Hash de contrasenas | Werkzeug `generate_password_hash` / `check_password_hash` (pbkdf2:sha256) |
| 3 | Validacion de entradas | Expresion regular de lista blanca `^[a-zA-Z0-9_.]+$`, maximo 50 caracteres |
| 4 | Limitacion de peticiones | Flask-Limiter (200 peticiones/dia, 50/hora por IP) |
| 5 | Cookies de sesion seguras | `HttpOnly`, `Secure`, `SameSite=Lax` |
| 6 | Cabeceras HTTP de seguridad | CSP, X-XSS-Protection, X-Frame-Options, HSTS |
| 7 | Terminacion TLS | Proxy inverso Nginx con HTTPS (certificados autofirmados para desarrollo) |
| 8 | Principio de minimo privilegio | Usuario no root `appuser` dentro del contenedor Docker |
| 9 | Control de acceso | Decorador `@login_required` en rutas protegidas |
| 10 | Sin secretos hardcodeados | `SECRET_KEY` obtenida desde variable de entorno |

---

## Construido Con

- **Flask 3.0** -- Framework web
- **Flask-SQLAlchemy 3.1** -- ORM y gestion de base de datos
- **Flask-Login 0.6** -- Gestion de sesiones de usuario
- **Flask-Limiter 3.7** -- Limitacion de peticiones
- **Werkzeug 3.0** -- Utilidades de hash de contrasenas
- **Gunicorn 22** -- Servidor WSGI para produccion
- **Nginx** -- Proxy inverso con terminacion TLS
- **Docker / Docker Compose** -- Contenedores y orquestacion
- **SQLite** -- Motor de base de datos (desarrollo)

---

## Primeros Pasos

### Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- (Opcional) Docker y Docker Compose

### Instalacion

Sigue estos pasos para ejecutar la aplicacion localmente:

**1. Clonar el repositorio**

```bash
git clone https://github.com/EmaConor/PoC.git
cd PoC
```

**2. Crear y activar un entorno virtual**

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

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar las variables de entorno**

Copia el archivo de ejemplo y ajusta los valores:

```bash
cp .env.example .env
```

Abre `.env` y configura las siguientes variables:

| Variable | Descripcion | Valor por defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Se usa para firmar sesiones y tokens CSRF. Genera una clave fuerte y aleatoria. | `change-this-to-a-random-secret-key` |
| `DATABASE_URL` | Cadena de conexion a la base de datos. Ruta SQLite para desarrollo, PostgreSQL/MySQL para produccion. | `sqlite:///app.db` |
| `FLASK_ENV` | Entorno de la aplicacion. Usar `development` para modo debug o `production` para configuracion hardening. | `development` |

> Para produccion, genera una `SECRET_KEY` segura:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

**5. Inicializar la base de datos**

Crea las tablas e inserta los usuarios de prueba:

```bash
python init_db.py
```

**6. Ejecutar la aplicacion**

```bash
python app.py
```

El servidor se iniciara en **http://127.0.0.1:5000**.

---

### Ejecutar con Docker

Para un entorno similar a produccion con Nginx y HTTPS:

```bash
docker-compose up --build -d
docker-compose exec web python init_db.py
```

Esto inicia dos contenedores:
- **web** -- Aplicacion Flask detrás de Gunicorn en el puerto 5000 (solo interno)
- **nginx** -- Proxy inverso con TLS en los puertos 80 y 443

Accede a la aplicacion en **https://localhost**.

---

## Credenciales por Defecto

El script de inicializacion crea los siguientes usuarios de prueba:

| Usuario | Contrasena | Rol |
|---------|------------|-----|
| admin | admin123 | admin |
| ema | emaema | user |
| yuri | yuri123 | user |
| gene | gene123 | user |

---

## Endpoints de la API

| Ruta | Metodo | Descripcion | Auth Requerida |
|------|--------|-------------|----------------|
| `/` | GET, POST | Pagina de inicio de sesion. POST envia credenciales para autenticacion. | No |
| `/dashboard` | GET | Panel protegido que muestra informacion del usuario autenticado. | Si |
| `/logout` | GET | Finaliza la sesion y redirige al login. | Si |

---

## Estructura del Proyecto

```
PoC/
├── app.py                 # Punto de entrada de la aplicacion Flask (rutas, cabeceras de seguridad, rate limiting)
├── config.py              # Clases de configuracion (Development, Production)
├── models.py              # Modelo User de SQLAlchemy con hash de contrasenas
├── init_db.py             # Inicializador de base de datos (crea tablas + usuarios de prueba)
├── requirements.txt       # Dependencias de Python
├── .env                   # Variables de entorno (no se incluye en el repositorio)
├── .env.example           # Plantilla de variables de entorno
├── Dockerfile             # Build multi-etapa de Docker
├── docker-compose.yml     # Orquestacion con Docker Compose (Flask + Nginx)
├── nginx/
│   ├── nginx.conf         # Configuracion de Nginx (HTTPS, proxy inverso)
│   └── certs/             # Certificados SSL (autofirmados para desarrollo)
├── templates/
│   ├── login.html         # Plantilla del formulario de inicio de sesion
│   └── dashboard.html     # Plantilla del panel de control
└── instance/
    └── app.db             # Archivo de base de datos SQLite (generado en tiempo de ejecucion)
```

---

## Configuracion

### Variables de Entorno

Toda la configuracion en tiempo de ejecucion se carga desde el archivo `.env` (ver `.env.example`):

- **SECRET_KEY** -- Cadena aleatoria usada para firmas criptograficas. Requerida en produccion.
- **DATABASE_URL** -- URI de la base de datos. Por defecto `sqlite:///app.db`.
- **FLASK_ENV** -- Controla el modo `development` vs `production`. En modo produccion, debug esta desactivado, testing esta apagado y la proteccion CSRF esta habilitada.

### Clases de Configuracion

Definidas en `config.py`:

| Configuracion | Development | Production |
|---------------|-------------|------------|
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

[Read in English](README.md)
