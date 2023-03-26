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
	pip install -e .

# Python venv setup
venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	make reqs
	@echo "=========="
	@echo "Virtual environment successfully created. To activate the venv:"
	@echo " \033[0;32msource .venv/bin/activate"

# Perform base setup
setup:
	docker swarm init
	docker-compose -f setup-compose.yml up --detach

setup/buckets:
	mc config host add minio http://localhost:9000 minio_admin minio_password
	mc mb --ignore-existing minio/raw-data
	mc mb --ignore-existing minio/processed-data
	mc mb --ignore-existing minio/enriched-data

teardown:
	docker swarm leave --force