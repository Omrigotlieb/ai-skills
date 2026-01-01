# CLAUDE.md Template: Django Project

A comprehensive template for Django web applications.

```markdown
# Project: [Name]

## Tech Stack
- **Framework:** Django 5.x
- **Python:** 3.12+
- **Database:** PostgreSQL 16
- **Cache:** Redis
- **Task Queue:** Celery

## Project Structure
```
project/
├── config/               # Django settings
│   ├── settings/
│   │   ├── base.py      # Common settings
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/           # User app
│   ├── core/            # Shared app
│   └── api/             # DRF API
├── templates/           # Jinja2/Django templates
├── static/              # Static files
└── manage.py
```

## Django Patterns

### Models
```python
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### Views
- Prefer class-based views (CBVs)
- Use ViewSets for DRF APIs
- Keep views thin, logic in services

### Services Layer
```python
# apps/users/services.py
class UserService:
    @staticmethod
    def create_user(email: str, password: str) -> User:
        # Business logic here
        pass
```

## Commands
```bash
# Development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser

# Testing
pytest
pytest --cov=apps

# Production
python manage.py collectstatic
gunicorn config.wsgi:application
```

## Testing
- **Framework:** pytest-django
- **Factories:** factory_boy
- **Coverage target:** 80%+
- **API tests:** Use DRF test client

## Environment Variables
```bash
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
```

## Code Standards
- Follow Django coding style
- Use type hints (Django-stubs)
- Docstrings for all public methods
- Keep apps focused and small

## Security
- CSRF protection enabled
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- HTTPS in production
```

---

## Django REST Framework

When using DRF:

```python
# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
        read_only_fields = ['id']

# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
```
