IMAGE_NAME = data-pipeline

DATA_DIR = $(PWD)/data

# Removes the container automatically when the execution finishes
DOCKER_RUN = docker run --rm -v $(DATA_DIR):/app/data

build:
	docker build -t $(IMAGE_NAME) .

dev:
	$(DOCKER_RUN) -e APP_ENV=dev $(IMAGE_NAME)

prod:
	$(DOCKER_RUN) -e APP_ENV=prod $(IMAGE_NAME)

smoke-dev:
	$(DOCKER_RUN) -e APP_ENV=dev $(IMAGE_NAME) --smoke

smoke-prod:
	$(DOCKER_RUN) -e APP_ENV=prod $(IMAGE_NAME) --smoke

# To clean containers and images (optional)
clean:
	docker rmi -f $(IMAGE_NAME) || true