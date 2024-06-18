# Variables
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_FILE = docker-compose.yml

# Targets
.PHONY: start stop restart remove clean

start:
	@echo "Starting Docker containers..."
	sudo $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

stop:
	@echo "Stopping Docker containers..."
	sudo $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

restart: stop start

remove:
	@echo "Removing Docker containers..."
	sudo $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --volumes --remove-orphans

clean:
	@echo "Cleaning up Docker containers and volumes..."
	sudo $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --volumes --rmi all --remove-orphans

status:
	@echo "Checking Docker containers status..."
	sudo $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

# Help
help:
	@echo "Makefile commands:"
	@echo "  make start   - Start Docker containers"
	@echo "  make stop    - Stop Docker containers"
	@echo "  make restart - Restart Docker containers"
	@echo "  make remove  - Remove Docker containers and associated volumes"
	@echo "  make clean   - Remove Docker containers, volumes, and images"
	@echo "  make status  - Check the status of Docker containers"