# Events Management (TechHub)

Django-based seminar management app with modal authentication, event registration, and profile dashboard.

## Tech Stack
- Backend: Django 4.2
- Frontend: Tailwind CSS (local build), custom JS
- Database: SQLite (portfolio-friendly default)
- Production runtime: Gunicorn + WhiteNoise

## Local Development

### 1. Clone and enter project
```bash
git clone https://github.com/qkgalias/events_management.git
cd events_management
```

### 2. Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend assets (Tailwind local build)
```bash
npm install
npm run build:css
```

For active frontend editing:
```bash
npm run watch:css
```

### 4. Environment variables
Create `.env` in project root.

```env
# Core
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost

# Security toggles (recommended for production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
USE_X_FORWARDED_HOST=True

# Email
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### 5. Database and run
```bash
python manage.py migrate
python manage.py loaddata dummy_data.json
python manage.py createsuperuser
python manage.py runserver
```

Open: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Docker Deployment

### 1. Build and run
```bash
docker compose up -d --build
```

App runs on port `8000`.

### 2. Production env recommendations
For production in `.env`:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## Cloudflare + Nginx Proxy Manager

### Cloudflare
- SSL/TLS mode: `Full (strict)`
- DNS record: point your domain/subdomain to your server IP (proxied)

### Nginx Proxy Manager
- Forward Host: your Docker host (or service host)
- Forward Port: `8000`
- Enable:
  - `Websockets Support`
  - `Block Common Exploits`
  - SSL certificate (Let's Encrypt)
  - `Force SSL`

After enabling SSL, ensure your `.env` has production values (`DEBUG=False`, secure cookie/HSTS flags enabled).

## Backup Notes (SQLite + media)
For portfolio deployments, backup these paths regularly:
- `db.sqlite3`
- `media/`

Example backup:
```bash
tar -czf backup-$(date +%F).tar.gz db.sqlite3 media
```

## Security Checklist
- Do not commit `.env`
- Use a strong random `SECRET_KEY`
- Keep `DEBUG=False` in production
- Set explicit `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Use HTTPS end-to-end with Cloudflare + NPM

## Verification Commands
```bash
python manage.py check --deploy
python manage.py test
python manage.py collectstatic --noinput
```
