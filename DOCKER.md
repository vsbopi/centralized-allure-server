# Docker Deployment Guide

This guide covers deploying the Centralized Allure Reports Server using Docker.

## Quick Start

### Prerequisites

- Docker installed and running
- Docker Compose (optional, but recommended)
- AWS credentials configured

### 1. Simple Docker Run

```bash
# Build the image
docker build -t allure-reports-server .

# Run the container
docker run -d \
  --name allure-reports \
  -p 8080:8080 \
  --env-file .env \
  --restart unless-stopped \
  allure-reports-server
```

### 2. Docker Compose (Recommended)

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Available Docker Files

### 1. `Dockerfile` (Development)
- Basic Python 3.11 slim image
- Includes development tools
- Good for development and testing

### 2. `Dockerfile.production` (Production)
- Multi-stage build for smaller image size
- Optimized for production deployment
- Security hardened with non-root user

### 3. `docker-compose.yml` (Production)
- Production-ready configuration
- Includes health checks
- Network configuration
- Volume mounts for logs

### 4. `docker-compose.dev.yml` (Development)
- Development configuration
- Source code mounted as volume
- Debug mode enabled
- Hot reload support

## Build Scripts

### Linux/Mac
```bash
# Build image
./docker-build.sh [tag] [dockerfile]

# Run container
./docker-run.sh [tag] [port]
```

### Windows
```batch
# Build image
docker-build.bat [tag] [dockerfile]

# Run container
docker-run.bat [tag] [port]
```

## Environment Configuration

Create a `.env` file with your AWS credentials:

```env
S3_BUCKET_NAME=your-allure-reports-bucket
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
PORT=8080
DEBUG=false
```

## Production Deployment

### 1. Using Production Dockerfile

```bash
# Build optimized production image
docker build -f Dockerfile.production -t allure-reports-server:prod .

# Run with production settings
docker run -d \
  --name allure-reports-prod \
  -p 80:8080 \
  --env-file .env \
  --restart unless-stopped \
  --memory="512m" \
  --cpus="0.5" \
  allure-reports-server:prod
```

### 2. With Reverse Proxy (Nginx)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  allure-reports:
    build:
      context: .
      dockerfile: Dockerfile.production
    environment:
      - PORT=8080
      - DEBUG=false
    env_file:
      - .env
    networks:
      - internal

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - allure-reports
    networks:
      - internal

networks:
  internal:
    driver: bridge
```

## Health Checks

The container includes health checks:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' allure-reports

# Manual health check
curl http://localhost:8080/health
```

## Logging

```bash
# View real-time logs
docker logs -f allure-reports

# View last 100 lines
docker logs --tail 100 allure-reports
```

## Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker logs allure-reports
   
   # Check if port is in use
   netstat -tulpn | grep 8080
   ```

2. **S3 connection issues**
   ```bash
   # Verify environment variables
   docker exec allure-reports env | grep AWS
   
   # Test S3 access
   docker exec -it allure-reports python -c "import boto3; print(boto3.client('s3').list_buckets())"
   ```

3. **Permission issues**
   ```bash
   # Check container user
   docker exec allure-reports whoami
   
   # Check file permissions
   docker exec allure-reports ls -la /app
   ```

## Scaling

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Create service
docker service create \
  --name allure-reports \
  --replicas 3 \
  --publish 8080:8080 \
  --env-file .env \
  allure-reports-server
```

### Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: allure-reports
spec:
  replicas: 3
  selector:
    matchLabels:
      app: allure-reports
  template:
    metadata:
      labels:
        app: allure-reports
    spec:
      containers:
      - name: allure-reports
        image: allure-reports-server:prod
        ports:
        - containerPort: 8080
        env:
        - name: S3_BUCKET_NAME
          value: "your-bucket"
        # Add other env vars from secrets
---
apiVersion: v1
kind: Service
metadata:
  name: allure-reports-service
spec:
  selector:
    app: allure-reports
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## Security Considerations

1. **Non-root user**: Containers run as `appuser`
2. **Minimal image**: Based on Python slim image
3. **No secrets in image**: Environment variables only
4. **Health checks**: Built-in container health monitoring
5. **Resource limits**: Set memory and CPU limits in production

## Performance Tuning

```bash
# Run with resource limits
docker run -d \
  --name allure-reports \
  --memory="1g" \
  --cpus="1.0" \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  allure-reports-server
```

## Backup and Monitoring

Since the application is stateless (all data in S3), focus on:

1. **Configuration backup**: Backup `.env` and docker-compose files
2. **Monitoring**: Use Docker stats and health checks
3. **Logging**: Centralized logging with ELK stack or similar

```bash
# Monitor container stats
docker stats allure-reports

# Export container metrics
docker inspect allure-reports
```
