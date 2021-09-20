# Image API

> 

## Technologies

- Django
- Django REST framework
- PostgreSQL
- Docker

## Setup

### To run the application:

```
$ docker-compose build
$ docker-compose up
$ docker-compose run --rm app sh -c "python manage.py makemigrations"
$ docker-compose run --rm app sh -c "python manage.py createsuperuser"
```