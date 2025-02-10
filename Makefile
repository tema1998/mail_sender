start:
	docker compose up --build

run-db:
	docker compose up pgdb

run-app:
	cd src && cd mail_sender && python manage.py runserver

run-migrate:
	cd src && cd mail_sender && python manage.py makemigrations && python manage.py migrate