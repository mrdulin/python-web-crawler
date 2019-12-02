# python-web-crawler

Python web crawler

Start mongodb server:

```bash
docker run --name mongodb -d --env-file ./.env -p 27017:27017 bitnami/mongodb:latest
```

`.env`:

```text
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_ROOT_PASSWORD=python-web-crawler-adminpass
MONGODB_DATABASE=python-web-crawler
MONGODB_USERNAME=python-web-crawler-testuser
MONGODB_PASSWORD=python-web-crawler-testpass
```
