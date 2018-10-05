dropdb --username=postgres repit
createdb --username=postgres repit
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
find . -path "*/fixtures/*.json" -not -name "hmac-drbg-nist.json" > fixtures.json
FOR /F %%i IN (.\fixtures.json) DO (
  python manage.py loaddata %%i
)
rm fixtures.json