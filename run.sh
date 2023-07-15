python3 manage.py makemigrations 
python3 manage.py migrate

if [ ! -d "staticfiles" ]; then
    python3 manage.py collectstatic --no-input
fi

gunicorn -c ./gunicorn/config.py user_manager_sys.wsgi
