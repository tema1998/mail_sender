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
<image src="src/mail_sender/static/images/tasks.jpg" alt="Screenshot of Tasks page">
<image src="src/mail_sender/static/images/history.jpg" alt="Screenshot of History page">

### Settings
Create .env file using .env.example.

### Install dependencies
First of all activate virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
```
pip install requirements.txt
```

### Local development
Run DB:
```
make run-db
```
Run app(without workers):
```
make run-app
```
To run migration:
```
make run-migration
```

### Makefile

To run app with db and workers docker(migrations will be run automatically):
```
make start
```
### Settings
To create task's intervals in the admin panel. I advise you to create intervals minimum 1 hour to avoid
problems with email blocking. Users will be able to send emails every 1 hour automatically:
```
http://127.0.0.1:8000/admin/django_celery_beat/intervalschedule/
```

[Docker]: https://img.shields.io/badge/docker-000000?style=for-the-badge&logo=docker&logoColor=blue
[Django]: https://img.shields.io/badge/django-000000?style=for-the-badge&logo=django&logoColor=white
[PostgreSQL]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql&logoColor=blue
[Celery]: https://img.shields.io/badge/celery-000000?style=for-the-badge&logo=celery&logoColor=green
[Redis]: https://img.shields.io/badge/redis-000000?style=for-the-badge&logo=redis&logoColor=red
