#!/bin/bash

# Docker run script for Allure Reports Server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="allure-reports-server"
TAG="${1:-latest}"
CONTAINER_NAME="allure-reports"
PORT="${2:-8080}"

echo -e "${YELLOW}Starting Allure Reports Server container...${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create a .env file with your AWS credentials:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your actual AWS credentials"
    exit 1
fi

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo -e "${YELLOW}Stopping existing container...${NC}"
    docker stop ${CONTAINER_NAME} >/dev/null 2>&1 || true
    docker rm ${CONTAINER_NAME} >/dev/null 2>&1 || true
fi

# Run the container
echo -e "${GREEN}Starting container...${NC}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8080 \
    --env-file .env \
    --restart unless-stopped \
    ${IMAGE_NAME}:${TAG}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Container started successfully!${NC}"
    echo ""
    echo "Container details:"
    docker ps -f name=${CONTAINER_NAME}
    echo ""
    echo "Access your allure reports at: http://localhost:${PORT}"
    echo ""
    echo "Useful commands:"
    echo "  View logs:     docker logs -f ${CONTAINER_NAME}"
    echo "  Stop:          docker stop ${CONTAINER_NAME}"
    echo "  Restart:       docker restart ${CONTAINER_NAME}"
    echo "  Shell access:  docker exec -it ${CONTAINER_NAME} /bin/bash"
    echo ""
    echo "Health check: curl http://localhost:${PORT}/health"
else
    echo -e "${RED}❌ Failed to start container!${NC}"
    exit 1
fi
