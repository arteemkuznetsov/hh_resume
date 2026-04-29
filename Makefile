COMPOSE = docker compose
SERVICE = hh-updater

.PHONY: up down rebuild logs status

up:
	@echo "Restarting..."
	$(COMPOSE) up -d --build --force-recreate

down:
	@echo "Exiting..."
	$(COMPOSE) down

rebuild:
	@echo "Full rebuilding..."
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d --force-recreate

logs:
	$(COMPOSE) logs -f $(SERVICE)

status:
	$(COMPOSE) ps