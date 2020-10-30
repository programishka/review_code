start:
	python3 manage.py runserver

deploy:
	git pull
	python3 manage.py migrate
	python3 manage.py collectstatic --noinput

bootstrap:
    pip3 install -r requirements.txt
    make deploy

setupvenv:
    pip3 install virtualenv
    virtualenv -ppython3 venv
