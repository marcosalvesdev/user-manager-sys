python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py collectstatic

gunicorn -c ./gunicorn/config.py user_manager_sys.wsgi
