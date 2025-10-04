# setup.sh - Run this script to set up the entire application
#!/bin/bash

echo "Setting up NCSU Marketplace Microservices..."

# Create project structure
mkdir -p ncsu-marketplace/{auth-service,listings-service,messaging-service}

# Create auth-service files
mkdir -p ncsu-marketplace/auth-service
cat > ncsu-marketplace/auth-service/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
EOF

# Create listings-service files
cat > ncsu-marketplace/listings-service/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
httpx==0.25.2
pydantic==2.5.0
pydantic-settings==2.1.0
EOF

# Create messaging-service files
cat > ncsu-marketplace/messaging-service/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
httpx==0.25.2
pydantic==2.5.0
pydantic-settings==2.1.0
EOF

echo "Project structure created!"
echo "Next steps:"
echo "1. Copy the provided Python files to their respective service directories"
echo "2. Copy the docker-compose.yml to the root directory"
echo "3. Run: docker-compose up --build"
