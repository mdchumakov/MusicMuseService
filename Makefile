createsuperuser:
	@poetry run python manage.py createsuperuser

collectstatic:
	@poetry run python manage.py collectstatic

runserver:
	@poetry run python manage.py runserver

migrate:
	@poetry run python manage.py migrate

format:
	@poetry run ruff format .

lint:
	@poetry run ruff check --fix .

make-migrations-music:
	@poetry run python manage.py makemigrations music

update-requirements:
	@poetry export -f requirements.txt --output requirements.txt --with docs --without-hashes

update-requirements-without-version:
	@poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt

opensearch-index-create:
	@poetry run python manage.py opensearch index create

opensearch-index-rebuild:
	@poetry run python manage.py opensearch index rebuild

opensearch-document:
	@poetry run python manage.py opensearch document index

squash-migrations:
	@poetry run python manage.py squashmigrations <appname> <squashfrom> <squashto>

django-shell:
	@poetry run python manage.py shell
