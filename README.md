# NCSU Marketplace - Microservices Implementation

A marketplace application for NCSU students built with microservices architecture.

## Architecture

### Services
1. **Authentication Service** (Port 8001)
   - User registration and login
   - JWT token management
   - User profile management

2. **Listings Service** (Port 8002)
   - CRUD operations for marketplace listings
   - Search and filtering capabilities
   - Category management

3. **Messaging Service** (Port 8003)
   - Conversation management between buyers and sellers
   - Real-time messaging
   - Message history

### Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose
- **Architecture**: Microservices with service-to-service communication

## Project Structure
```
ncsu-marketplace/
├── docker-compose.yml
├── auth-service/
│   ├── main.py
│   ├── controller.py
│   ├── service.py
│   ├── models.py
│   ├── schemas.py
│   ├── config.py
│   ├── database.py
│   ├── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── listings-service/
│   ├── main.py
│   ├── controller.py
│   ├── service.py
│   ├── models.py
│   ├── schemas.py
│   ├── config.py
│   ├── database.py
│   ├── auth_client.py
│   ├── requirements.txt
│   └── Dockerfile
└── messaging-service/
    ├── main.py
    ├── controller.py
    ├── service.py
    ├── models.py
    ├── schemas.py
    ├── config.py
    ├── database.py
    ├── external_clients.py
    ├── requirements.txt
    └── Dockerfile
```

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd ncsu-marketplace
   ```

2. **Start Services**
   ```bash
   docker-compose up --build
   ```

3. **Test APIs**
   ```bash
   python3 test_api.py
   ```

## API Endpoints

### Authentication Service (localhost:8001)
- `POST /v1/auth/register` - Register new user
- `POST /v1/auth/login` - User login
- `GET /v1/auth/me` - Get current user profile
- `PATCH /v1/auth/me` - Update user profile
- `GET /v1/auth/validate` - Validate token (internal)

### Listings Service (localhost:8002)
- `GET /v1/listings/` - Get all listings with filters
- `POST /v1/listings/` - Create new listing
- `GET /v1/listings/{id}` - Get specific listing
- `PATCH /v1/listings/{id}` - Update listing
- `DELETE /v1/listings/{id}` - Delete listing

### Messaging Service (localhost:8003)
- `GET /v1/conversations/` - Get user conversations
- `POST /v1/conversations/` - Start new conversation
- `GET /v1/conversations/{id}/messages` - Get conversation messages
- `POST /v1/conversations/{id}/messages` - Send message

## Inter-Service Communication

- **Listings → Auth**: Validates user tokens for protected endpoints
- **Messaging → Auth**: Validates user tokens for protected endpoints  
- **Messaging → Listings**: Fetches listing details when creating conversations

## Database Schema

### Auth Service
- `users` table with user credentials and profile information

### Listings Service
- `listings` table with product information, pricing, and seller details

### Messaging Service
- `conversations` table linking buyers, sellers, and listings
- `messages` table storing conversation messages

## Features Implemented

✅ User registration and authentication
✅ JWT token-based security
✅ CRUD operations for listings
✅ Search and filtering for listings
✅ Conversation management
✅ Message sending and retrieval
✅ Inter-service communication
✅ Dockerized deployment
✅ Database persistence

## Development Notes

- Each service follows a layered architecture (Controller → Service → Model)
- Services communicate via HTTP REST APIs
- PostgreSQL databases are isolated per service
- JWT tokens are used for authentication across services
- Docker Compose manages the entire application stack

## Testing

Use the provided `test_api.py` script to test basic functionality:

```bash
# Start services
docker-compose up -d

# Wait for services to be ready, then test
python3 test_api.py
```

## Production Considerations

- Replace JWT secrets with secure, environment-specific values
- Implement proper error handling and logging
- Add API rate limiting
- Consider adding API Gateway for external access
- Implement service discovery for dynamic service communication
- Add monitoring and health checks
