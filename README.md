AuthService 🛡️

AuthService is a Django-based authentication microservice that provides secure user management and authentication, backed by PostgreSQL and Redis.

🚀 Features

User registration and login

JWT-based authentication

Password hashing and secure storage

PostgreSQL database for persistence

Redis support (for caching, sessions, or rate limiting)

Dockerized for easy deployment

SETUP

<!-- ## Clone the Repo -->
git clone https://github.com/21ntphilos/Django-Auth-system.git
cd authservice

<!-- ## Create vritual environment  -->
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate 


<!-- ## ENVs -->
# Django
SECRET_KEY=your_secret_key
DEBUG=True

# Database
DATABASE_URL=${POSTGRESS_DB_URL}

# Redis
REDIS_URL=redis://redis:6379/0

<!-- ## RUN Migration  -->
python manage.py migrate


<!-- ## RUN Locally  -->
python manage.py runserver


<!-- ## Running with Docker -->
1. Build Containers -->
    docker compose build

2. Start Containers
    docker compose up -d

3. Apply Migrations in the Web Container
    docker compose exec web python manage.py migrate


<!-- API Documentation -->
Authentication Endpoints
1. Register a User

    POST {{baseUrl}}api/accounts/register/
    Content-Type: application/json

    {
    "full_name": "Fillibister",
    "email": "hbt@gmail.com",
    "password": "tell me more"
    }

    Response:

    {
    "id": 1,
    "full_name": "Fillibister",
        "email": "hbt@gmail.com",
    }

2. Login

POST {{baseUrl}}api/accounts/login/
Content-Type: application/json

{
  "email": "hbt@gmail.com",
  "password": "tell me more"
}


Response:

{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}

3. Refresh Token

POST {{baseUrl}}api/accounts/token/refresh/

{
  "refresh": "jwt_refresh_token"
}


Response:

{
  "access": "new_jwt_access_token"
}
