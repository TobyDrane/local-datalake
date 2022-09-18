-include .env
export

brew:
	brew bundle

pre-commit-setup:
	pre-commit install

python-setup: brew pre-commit-setup
	pyenv install --skip-existing 3.8.12
	echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
	pyenv local 3.8.12

# Install all requirements
reqs:
	pip install -r requirements.txt

# Python venv setup
venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	make reqs
	@echo "=========="
	@echo "Virtual environment successfully created. To activate the venv:"
	@echo " \033[0;32msource .venv/bin/activate"

# Perform base setup
pre-setup:
ifeq ($(minio_access_key), )
	@echo "\033[0;31m--- You have not replaced the minio access key value."
else ifeq ($(minio_secret_key), )
	@echo "\033[0;31m--- You have not replaced the minio secret access key value."
else
	docker swarm init
	printf "$(minio_access_key)" | docker secret create access_key -
	printf "$(minio_secret_key)" | docker secret create secret_key -
endif

setup:
	docker compose -f setup-compose.yml up --detach

	mc config host add minio http://localhost:4003 minio_admin minio_password
	mc mb --ignore-existing minio/raw-data
	mc mb --ignore-existing minio/processed-data
	mc mb --ignore-existing minio/enriched-data

teardown:
	docker swarm leave --force