# urlnk.io
A simple URL shortener.

# Project setup
Build and run dev environment:
```shell
docker compose --project-name urlnk up --build
```

Test if container is running:
```shell
curl -X GET "http://127.0.0.1:8000/health"
```

Shorten a URL:
```shell
curl -X POST "http://127.0.0.1:8000/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.google.com"}'
```
