web: gunicorn syntaxforest.wsgi --workers 2 --threads 2 --log-file -
searchworker: python manage.py syntaxforestsearch
taskworker: python manage.py syntaxforesttask
release: python manage.py migrate
