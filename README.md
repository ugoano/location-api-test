# Localistico technical test

## Start the web server

Install redis-server either from `docker` or with `apt-get install`

Change directory to `localisticoapi/`

```
python manage.py runserver
```


## Testing

Start the server.

Change to the same directory of this README

```
python setup.py develop
pytest tests/
```
