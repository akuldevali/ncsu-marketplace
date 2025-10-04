.PHONY: build up down logs test clean

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	python3 test_api.py

clean:
	docker-compose down -v
	docker system prune -f

dev:
	docker-compose up --build