# Localistico technical test

## Server setup

* Install redis-server either from `docker` or with `apt-get install`

```
docker run --name my-redis -d redis
```

* Monitor `callback_url` on `http://localhost:8081` in a separate terminal:

```
./callback_listener.sh
```

* Change directory to `localisticoapi/`

```
cd localisticoapi
```

* Start the Celery worker in a separate terminal

```
celery worker -A localisticoapi --loglevel=debug
```

* Start the Django web server in a separate terminal

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

## Using the API

In order to see the code differences in the final two questions, I created a new endpoint for the async call.  The URLs are as follows for synchronous gsearch and asynchronous gsearch respectively:

```
http://localhost:8000/gsearch/?params
```

Parameters:
query (required)
latitude (optional)
longitude (optional)

```
http://localhost:8000/gsearch/async/?params
```

Parameters:
query (required)
callback_url (required)
latitude (optional)
longitude (optional)

## Future

I tried to balance a fine line between getting the code done and doing it right.  But here are a few notes:

* Had to refamiliarise myself with Django, and had only used Celery with Flask a few years ago, so there could be better or more industry-standard ways of doing this.
* If I had the time I would use `docker` to start the web server, use a web server for the `nc` listener, install the dependencies, start the Celery worker, as well as the Redis broker so that running the tests are a lot simpler.
* I feel some more refactoring can be done in the sync-async endpoints.
* Generated a proper API doc
* More thorough testing of the edge cases (I didn't cover all of them).
