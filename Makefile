install:
	uv sync

run:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest -v

docker-build:
	docker build -t usuario/signalforhelp-backend:latest .

docker-run:
	docker run -p 8000:8000 usuario/signalforhelp-backend:latest
