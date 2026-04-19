# JobMatch Backend — Django REST API

## Структура проекта

```
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── models.py       # User, Resume, Favorite, Notification
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py      # Фильтры для поиска
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Установка и запуск

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

Также нужен `django-filter`:
```bash
pip install django-filter
```

### 2. Создать базу данных PostgreSQL

Открой pgAdmin или psql и выполни:
```sql
CREATE DATABASE jobmatch;
```

### 3. Создать `.env` файл

Скопируй `.env.example` → `.env` и заполни:
```
SECRET_KEY=любой-случайный-текст
DEBUG=True
DB_NAME=jobmatch
DB_USER=postgres
DB_PASSWORD=твой_пароль
DB_HOST=localhost
DB_PORT=5432
```

### 4. Применить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создать суперпользователя (для админки)

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

Бэк запустится на: **http://localhost:8000**

---

## API эндпоинты

### Авторизация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/auth/register/` | Регистрация |
| POST | `/api/auth/login/` | Вход, возвращает JWT токены |
| POST | `/api/auth/refresh/` | Обновить access токен |
| GET | `/api/auth/me/` | Данные текущего пользователя |
| PATCH | `/api/auth/me/` | Обновить профиль |
| POST | `/api/auth/change-password/` | Сменить пароль |

### Резюме (работник)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/resumes/` | Мои резюме |
| POST | `/api/resumes/` | Создать резюме |
| GET | `/api/resumes/{id}/` | Одно резюме |
| PUT/PATCH | `/api/resumes/{id}/` | Редактировать |
| DELETE | `/api/resumes/{id}/` | Удалить |

### Поиск (работодатель)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/search/` | Все резюме с фильтрами |

**Параметры фильтрации:**
```
?profession=programmer
?level=senior
?city=almaty
?experience_min=2
?experience_max=10
?has_bachelor=true
?has_master=true
?language=english
?search=Иванов       ← поиск по имени/фамилии/о себе
?ordering=-experience_years
```

### Избранное (работодатель)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/favorites/` | Список избранных |
| POST | `/api/favorites/toggle/{resume_id}/` | Лайк/анлайк |

### Уведомления (работник)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/notifications/` | Все уведомления |
| POST | `/api/notifications/read/` | Пометить все прочитанными |
| GET | `/api/notifications/unread-count/` | Счётчик непрочитанных |

---

## Как использовать JWT токены

После логина/регистрации в ответе придёт:
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": { ... }
}
```

В Angular добавляй в каждый запрос:
```
Authorization: Bearer <access_token>
```

Когда access токен истечёт — отправь refresh на `/api/auth/refresh/` чтобы получить новый.

---

## Переключение между аккаунтами

Просто храни несколько токенов в Angular (например в localStorage):
```javascript
// Сохранить токен аккаунта
localStorage.setItem('token_worker', accessToken)
localStorage.setItem('token_employer', accessToken)

// Переключиться — просто поменять активный токен
localStorage.setItem('active_token', localStorage.getItem('token_employer'))
```

Все данные хранятся в PostgreSQL — ничего не теряется при переключении.

---

## Админка

Доступна по адресу: **http://localhost:8000/admin/**
