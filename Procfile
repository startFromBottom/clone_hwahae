web: gunicorn myapp.config.wsgi --log-file -
migrate: python manage.py migrate --settings=myapp.config.settings.production
seed: python manage.py loaddata myapp/item/fixtures/items-data.json