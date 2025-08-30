#!/bin/bash

# Docker build script for Allure Reports Server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="allure-reports-server"
TAG="${1:-latest}"
DOCKERFILE="${2:-Dockerfile}"

echo -e "${YELLOW}Building Allure Reports Server Docker image...${NC}"
echo "Image name: ${IMAGE_NAME}:${TAG}"
echo "Dockerfile: ${DOCKERFILE}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Make sure to set environment variables when running the container.${NC}"
fi

# Build the image
echo -e "${GREEN}Building Docker image...${NC}"
docker build -f ${DOCKERFILE} -t ${IMAGE_NAME}:${TAG} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
    echo ""
    echo "To run the container:"
    echo "  docker run -p 8080:8080 --env-file .env ${IMAGE_NAME}:${TAG}"
    echo ""
    echo "Or use Docker Compose:"
    echo "  docker-compose up"
    echo ""
    echo "Image details:"
    docker images ${IMAGE_NAME}:${TAG}
else
    echo -e "${RED}❌ Docker build failed!${NC}"
    exit 1
fi
