.PHONY: install run test migrate

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/test_students.py -v --timeout=30

migrate:
	flask db upgrade