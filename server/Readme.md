# Server

## Deploy

See [docs file](docs/Deploy.md).

## Quickstart

To start the server, run the following command:

```shell
$ docker-compose -f dev.yml up
```

If you don't have a Docker, make sure you have installed PostgreSQL and Python. Then do the following steps:

First, create a database with name *'django-messenger'* using PgAdmin or PSQL.

PSQL command:

```
# CREATE DATABASE "django-messenger";
```

Change the *'POSTGRES_USER'* and *'POSTGRES_PASSWORD'* fields to your own username and password in
this [file](env/local.env).

Then, install the dependencies:

```shell
$ pip install -r requirements.txt
```

**NOTE:** if you have Linux installed, change *'requirements.txt'* to *'requirements_deploy.txt'*.

And finally run the server:

```shell
$ ./scripts/runserver
```

Now the server is available [there](http://localhost:8000/).
