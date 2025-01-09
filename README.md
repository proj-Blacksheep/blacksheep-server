# Blacksheep Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
<!-- [![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/proj-Blacksheep/blacksheep-server) -->

A comprehensive LLM governance platform that enables monitoring LLM usage, managing users and models, and provides a unified interface for various LLM providers.

## Features

- User authentication and authorization
- Usage monitoring and rate limiting
- Support for multiple AI model providers
- RESTful API design
- Docker support

## Tech Stack

- Python 3.12+
- Blacksheep (ASGI web framework)
- SQLAlchemy (ORM)
- Poetry (Dependency Management)
- Docker & Docker Compose

## Installation

### Prerequisites

- Python 3.12
- Docker & Docker Compose
- LLM API credentials

### Using Docker

```bash
# Clone the repository
git clone https://github.com/proj-Blacksheep/blacksheep-server
cd blacksheep-server

# Build and run with Docker Compose
docker-compose up --build
```

### Local Development

```bash
# Install poetry
pip install poetry

# Install dependencies
poetry install

# Run the server
poetry run python -m src.main
```

## API Documentation

### Authentication

| Endpoint | Method | Description | Request Data |
|----------|---------|-------------|--------------|
| `/login` | POST | User login and token generation | username, password |

### User Management (`/users`)

#### Regular User Endpoints
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/users/me` | GET | Get current user information |
| `/users/usage/{username}` | GET | Get user's API usage |
| `/users/password` | POST | Change password |

#### Admin Endpoints
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/users/create` | POST | Create new user |
| `/users/all` | GET | Get all users information |
| `/users/{username}` | DELETE | Delete user |
| `/users/limit/{username}` | POST | Set user usage limits |

### Model Management
| Endpoint | Method | Description | Permission |
|----------|---------|-------------|------------|
| `/models/create` | POST | Create new model | Admin |
| `/models/all` | GET | List available models | All users |
| `/models/{model_name}` | DELETE | Delete model | Admin |

### Model Inference
| Endpoint | Method | Description | Request Data |
|----------|---------|-------------|--------------|
| `/api/call` | POST | Call AI model | model_name, prompt, max_tokens (optional), temperature (optional) |

## Supported AI Models

Currently supporting:
- Azure OpenAI
  - Required settings:
    - deployment_name
    - end_point
    - api_key

More providers coming soon!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Configuration

### Docker Configuration

The service can be configured through `docker-compose.yml`. Here's an example configuration:

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

For local development, configure the settings in `src/core/config.py`. The following settings are available:

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

## Support

If you have any questions or need help with setup, please open an issue on GitHub.
