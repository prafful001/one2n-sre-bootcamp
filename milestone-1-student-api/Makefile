.PHONY: install run test migrate docker-build docker-run

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/test_students.py -v --timeout=30

migrate:
	flask db upgrade

docker-build:
	docker build -t student-api:1.0.0 .

docker-run:
	docker run -p 5000:5000 \
		-e DATABASE_URL=$(DATABASE_URL) \
		-e FLASK_APP=$(FLASK_APP) \
		-e FLASK_ENV=$(FLASK_ENV) \
		-e SECRET_KEY=$(SECRET_KEY) \
		student-api:1.0.0