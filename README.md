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
curl -X POST "http://127.0.0.1:8000/api/urls" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.google.com"}'
```

Get all short URLs:
```shell
curl -X GET "http://127.0.0.1:8000/api/urls"
```

Get a short URL by database id:
```shell
curl -X GET "http://127.0.0.1:8000/api/urls/1"
```

Get a short URL by short code:
```shell
curl -X GET "http://127.0.0.1:8000/api/urls/shortcode/gDESx6"
```

Update a short URL source:
```shell
curl -X PUT "http://127.0.0.1:8000/api/urls/1" \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.yahoo.com"}'
```

Delete a short URL by database id:
```shell
curl -X DELETE "http://127.0.0.1:8000/api/urls/1"
```
