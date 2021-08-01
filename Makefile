deploy:
	git pull
	docker-compose up --build alias_db alias_web alias_nginx

run_docker:
	docker-compose up --build alias_docker alias_db

install_requirements:
	pip install -r ./.requirements/common.txt

install_linters:
	pip install -r ./.requirements/linters.txt
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate

lint:
	black alias
	isort alias
	flake8 alias
