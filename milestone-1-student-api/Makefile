.PHONY: install run test migrate docker-build docker-run start-db stop-db start-api

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/test_students.py -v --timeout=30

migrate:
	docker exec student-db psql -U postgres -d student_db -c "SELECT 1" && \
	flask db upgrade

docker-build:
	docker build -t student-api:1.0.0 .

docker-run:
	docker run -p 5000:5000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/student_db -e FLASK_APP=app -e FLASK_ENV=development -e SECRET_KEY=your-secret-key student-api:1.0.0

start-db:
	docker-compose up -d db
	@echo "Waiting for DB to be ready..."
	@timeout /t 5 /nobreak > nul

stop-db:
	docker-compose down

start-api: docker-build start-db migrate
	docker-compose up -d api
	@echo "API is running at http://localhost:5000"