# Mail-sender service

### Built With

* ![Docker][Docker]
* ![Django][Django]
* ![PostgreSQL][PostgreSQL]
* ![Celery][Celery]
* ![Redis][Redis]


Functions |
-- |
`Send email` |
`Send group email` |
`Create task for sending emails` |
`Manage tasks` |
`History` |
`Sign in / Sign up` |

### Screenshots
<image src="webapp/mail_sender/static/images/tasks.jpg" alt="Screenshot of Tasks page">
<image src="webapp/mail_sender/static/images/history.jpg" alt="Screenshot of History page">

### Settings
File `.env.dev` contains project, DB, email settings.
```
DEBUG=True
SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

SQL_ENGINE=django.db.backends.postgresql_psycopg2
SQL_DATABASE=postgres
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=pgdb
SQL_PORT=5432

EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587
```

### Run project
Migrations will be started automatically
```
docker-compose up -d --build
```
To create superuser - run after previous command:
```
docker exec -it container_id python ./mail_sender/manage.py createsuperuser
```

[Docker]: https://img.shields.io/badge/docker-000000?style=for-the-badge&logo=docker&logoColor=blue
[Django]: https://img.shields.io/badge/django-000000?style=for-the-badge&logo=django&logoColor=white
[PostgreSQL]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql&logoColor=blue
[Celery]: https://img.shields.io/badge/celery-000000?style=for-the-badge&logo=celery&logoColor=green
[Redis]: https://img.shields.io/badge/redis-000000?style=for-the-badge&logo=redis&logoColor=red
