createsuperuser:
	@poetry run python manage.py createsuperuser

collectstatic:
	@poetry run python manage.py collectstatic

runserver:
	@poetry run python manage.py runserver

migrate:
	@poetry run python manage.py migrate
