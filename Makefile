mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

l_make:
	django-admin makemessages -l uz
	django-admin makemessages -l en

l_compile:
	django-admin compilemessages