.PHONY: up down logs ps

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

deploy: up
	@echo "Deployment complete! API accessible at http://localhost:8080"