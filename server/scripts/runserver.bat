
echo "Apply database migrations"
python manage.py migrate


echo "Starting server"
python manage.py runserver 127.0.0.1:8000