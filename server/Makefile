run:
	uvicorn api:app --host 0.0.0.0 --port 8080 --reload

install:
	poetry install

reinstall: 
	make clean
	rm -rf .venv
	make install

lint:
	poetry run black .

clean: 
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache