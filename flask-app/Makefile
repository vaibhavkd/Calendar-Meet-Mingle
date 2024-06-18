# Variables
DOCKER_IMAGE_NAME = calendar_system
DOCKER_CONTAINER_NAME = calendar_system_container
DOCKER_PORT = 5000

# Targets
.PHONY: build start stop restart remove clean status help

build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

start:
	@echo "Starting Docker container..."
	docker run -d --name $(DOCKER_CONTAINER_NAME) -p $(DOCKER_PORT):$(DOCKER_PORT) --network host  $(DOCKER_IMAGE_NAME)

container-status:
	@echo "Checking Docker container status..."
	docker ps -a | grep $(DOCKER_CONTAINER_NAME)

stop:
	@echo "Stopping Docker container..."
	docker stop $(DOCKER_CONTAINER_NAME)

restart: stop start

remove:
	@echo "Removing Docker container..."
	docker rm $(DOCKER_CONTAINER_NAME)

clean: stop remove
	@echo "Cleaning up Docker image..."
	docker rmi $(DOCKER_IMAGE_NAME)

status:
	@echo "Checking Docker container status..."
	docker ps -a | grep $(DOCKER_CONTAINER_NAME)

logs:
	@echo "Get Docker container logs..."
	docker logs $(DOCKER_CONTAINER_NAME)

help:
	@echo "Makefile commands:"
	@echo "  make build   - Build Docker image"
	@echo "  make start   - Start Docker container"
	@echo "  make container-status - Check the status of Docker container"
	@echo "  make stop    - Stop Docker container"
	@echo "  make restart - Restart Docker container"
	@echo "  make remove  - Remove Docker container"
	@echo "  make clean   - Stop and remove Docker container and image"
	@echo "  make status  - Check the status of Docker container"
	@echo "  make help    - Display this help message"
