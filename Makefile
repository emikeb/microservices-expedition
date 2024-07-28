.PHONY: all api_gateway_tests product_service_tests user_service_tests clean coverage combine_coverage docker_up docker_down

all: test
test: run_tests combine_coverage
all_docker: docker_up test docker_down

# Services paths
API_GATEWAY_DIR = api_gateway
PRODUCT_SERVICE_DIR = services/product_service
USER_SERVICE_DIR = services/user_service

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

api_gateway_tests:
	cd $(API_GATEWAY_DIR) && poetry install --no-root && poetry run coverage run -m pytest && mv .coverage ../.coverage-api_gateway

product_service_tests:
	cd $(PRODUCT_SERVICE_DIR) && poetry install --no-root && poetry run coverage run -m pytest && mv .coverage ../../.coverage-product_service

user_service_tests:
	cd $(USER_SERVICE_DIR) && poetry install --no-root && poetry run coverage run -m pytest && mv .coverage ../../.coverage-user_service

run_tests: api_gateway_tests product_service_tests user_service_tests

combine_coverage:
	coverage combine .coverage-api_gateway .coverage-product_service .coverage-user_service
	coverage report
	coverage html

clean:
	cd $(API_GATEWAY_DIR) && poetry env remove --all --yes
	cd $(PRODUCT_SERVICE_DIR) && poetry env remove --all --yes
	cd $(USER_SERVICE_DIR) && poetry env remove --all --yes
	docker-compose down --volumes --remove-orphans
	rm -f .coverage-api_gateway .coverage-product_service .coverage-user_service