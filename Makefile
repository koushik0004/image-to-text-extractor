# Makefile
# Simplifies Docker Compose commands

.PHONY: help build up down restart logs clean test dev prod

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Image Text Extractor - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Build the Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker-compose build

up: ## Start the application (detached mode)
	@echo "$(BLUE)Starting application...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Application started at http://localhost:8501$(NC)"

down: ## Stop and remove containers
	@echo "$(BLUE)Stopping application...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Application stopped$(NC)"

restart: ## Restart the application
	@echo "$(BLUE)Restarting application...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ Application restarted$(NC)"

logs: ## View application logs (follow mode)
	docker-compose logs -f app

logs-tail: ## View last 50 lines of logs
	docker-compose logs --tail=50 app

ps: ## Show running containers
	docker-compose ps

dev: ## Start in development mode with hot-reload
	@echo "$(BLUE)Starting in development mode...$(NC)"
	docker-compose up
	@echo "$(GREEN)✓ Development mode started$(NC)"

prod: ## Start in production mode
	@echo "$(BLUE)Starting in production mode...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✓ Production mode started at http://localhost:8501$(NC)"

stop: ## Stop containers without removing them
	@echo "$(BLUE)Stopping containers...$(NC)"
	docker-compose stop
	@echo "$(GREEN)✓ Containers stopped$(NC)"

clean: ## Remove containers, images, and volumes
	@echo "$(RED)Cleaning up all resources...$(NC)"
	docker-compose down -v --rmi all
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

rebuild: ## Rebuild and restart (no cache)
	@echo "$(BLUE)Rebuilding without cache...$(NC)"
	docker-compose build --no-cache
	docker-compose up -d
	@echo "$(GREEN)✓ Rebuild complete$(NC)"

health: ## Check application health
	@echo "$(BLUE)Checking application health...$(NC)"
	@docker-compose ps
	@curl -f http://localhost:8501/_stcore/health && echo "$(GREEN)✓ Application is healthy$(NC)" || echo "$(RED)✗ Application is unhealthy$(NC)"

shell: ## Open shell in running container
	docker-compose exec app /bin/bash

test: ## Test the application
	@echo "$(BLUE)Testing application...$(NC)"
	@curl -f http://localhost:8501/_stcore/health && echo "$(GREEN)✓ Application is responding$(NC)" || echo "$(RED)✗ Application is not responding$(NC)"

stats: ## Show resource usage statistics
	docker stats image-text-extractor

validate: ## Validate docker-compose configuration
	@echo "$(BLUE)Validating configuration...$(NC)"
	docker-compose config
	@echo "$(GREEN)✓ Configuration is valid$(NC)"

update: ## Pull latest changes and rebuild
	@echo "$(BLUE)Updating application...$(NC)"
	git pull
	docker-compose build
	docker-compose up -d
	@echo "$(GREEN)✓ Application updated$(NC)"

backup: ## Backup .env file
	@echo "$(BLUE)Creating backup...$(NC)"
	cp .env .env.backup-$(shell date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)✓ Backup created$(NC)"