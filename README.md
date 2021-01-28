# hubs-bikes

[![Build Status](https://travis-ci.org/drewbrew/hubs-bikes.svg?branch=master)](https://travis-ci.org/drewbrew/hubs-bikes)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Bike repair tracking for HUBS Coop. Check out the project's [documentation](http://drewbrew.github.io/hubs-bikes/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
