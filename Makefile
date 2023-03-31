
LOCAL_COMPOSE_FILE_PATH = "local.yml"

# Run the project using docker-compose
build:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) build


up:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) up  -d  # --build

down:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) down --remove-orphans

updown:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) down --remove-orphans
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) up  -d


ps:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) ps

logs:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) logs -f payment_service_local_django


# Linters
lint:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django flake8

# For Pytest and coverage
test:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django pytest --disable-pytest-warnings
	#docker-compose -f $(LOCAL_COMPOSE_FILE_PATH) exec django run pytest -s --disable-pytest-warnings tests

coverage_tests:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django coverage run -m pytest

coverage_report:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django coverage report


# Django commands
migrations:
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django python manage.py makemigrations

migrate: migrations
	docker compose -f $(LOCAL_COMPOSE_FILE_PATH) run --rm django python manage.py migrate
