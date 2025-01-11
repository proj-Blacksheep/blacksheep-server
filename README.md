# Blacksheep Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

A comprehensive LLM governance platform that enables monitoring LLM usage, managing users and models, and provides a unified interface for various LLM providers.

## Key Features

- User Authentication and Authorization
- Usage Monitoring and Rate Limiting
- Multiple AI Model Provider Support
- RESTful API Design
- Docker Support

## Tech Stack

- Python 3.12+
- Blacksheep (ASGI Web Framework)
- SQLAlchemy (ORM)
- Poetry (Dependency Management)
- Docker & Docker Compose

## Installation

### Prerequisites

- Python 3.12 or higher
- Docker & Docker Compose
- LLM API Credentials

### Using Docker

```bash
# Clone the repository
git clone https://github.com/proj-Blacksheep/blacksheep-server
cd blacksheep-server

# Set up environment variables
cp .env.example .env
# Edit the .env file to configure your settings

# Build and run with Docker Compose
docker-compose up --build
```

### Local Development Setup

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit the .env file to configure your settings

# Run the server
poetry run python -m src.main
```

## API Documentation

### Authentication API (`/login`)

| Endpoint | Method | Description | Request Data | Response |
|----------|---------|-------------|--------------|----------|
| `/login` | POST | User login and token generation | `username`, `password` | `{"access_token": "token", "token_type": "bearer"}` |

### User Management API (`/users`)

#### Regular User Endpoints
| Endpoint | Method | Description | Request Data | Response |
|----------|---------|-------------|--------------|----------|
| `/users/me` | GET | Get current user information | - | User info |
| `/users/usage/{username}` | GET | Get user's API usage | - | Usage info |
| `/users/password` | POST | Change password | `current_password`, `new_password` | Success message |

#### Admin Endpoints
| Endpoint | Method | Description | Request Data | Response |
|----------|---------|-------------|--------------|----------|
| `/users/create` | POST | Create new user | `username`, `password`, `is_admin` | Success message |
| `/users/all` | GET | Get all users information | - | User list |
| `/users/{username}` | DELETE | Delete user | - | Success message |

### Model Management API (`/models`)

| Endpoint | Method | Description | Permission | Request Data | Response |
|----------|---------|-------------|------------|--------------|----------|
| `/models/create` | POST | Create new model | Admin | `model_name`, `model_type`, `model_endpoint`, `model_api_key` | Success message |
| `/models/all` | GET | List available models | All users | - | Model list |
| `/models/{model_name}` | DELETE | Delete model | Admin | - | Success message |

### Model Inference API (`/api`)

| Endpoint | Method | Description | Request Data | Response |
|----------|---------|-------------|--------------|----------|
| `/api/call` | POST | Call AI model | `model_name`, `prompt`, `max_tokens` (optional), `temperature` (optional) | Model response |

## Supported AI Models

Currently supporting:
- Azure OpenAI
  - Required settings:
    - `deployment_name`: Deployment name
    - `end_point`: API endpoint
    - `api_key`: API key

More providers coming soon!

## Configuration

### Docker Configuration

The service can be configured through `docker-compose.yml`. Example configuration:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - VERSION=1.0.0
      - ENVIRONMENT=production
      - SECRET_KEY=your-secret-key
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
      - DEFAULT_ADMIN_USERNAME=admin
      - DEFAULT_ADMIN_PASSWORD=admin
      - DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
      - DB_ECHO=false
```

### Local Configuration

For local development, configure the settings in `src/core/config.py`:

```python
# Application settings
VERSION = "1.0.0"                 # Application version
ENVIRONMENT = "development"       # Environment (development, staging, production)
SECRET_KEY = "your-secret-key"    # Secret key for JWT token encoding
ALGORITHM = "HS256"               # Algorithm used for JWT token encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Admin credentials
DEFAULT_ADMIN_USERNAME = "admin"  # Default admin username
DEFAULT_ADMIN_PASSWORD = "admin"  # Default admin password

# Database settings
DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"  # Database connection URL
DB_ECHO = False                   # Whether to echo SQL statements
```

All settings can be overridden using environment variables with the same name.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or need help with setup, please open an issue on GitHub.
