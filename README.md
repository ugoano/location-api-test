# Localistico technical test

## Start the web server

* Install redis-server either from `docker` or with `apt-get install`

```
docker run --name my-redis -d redis
```

* Change directory to `localisticoapi/`

```
cd localisticoapi
```

* Start the Django web server

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
