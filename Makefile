build:
	docker compose -f docker-compose.yaml build

start:
	docker compose -f docker-compose.yaml up -d

stop:
	docker compose -f docker-compose.yaml down

restart:
	docker compose -f docker-compose.yaml restart
