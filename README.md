# CountAPI

This project is a clone of the functionality available at https://countapi.xyz/ implemented with Python using [FastAPI](https://fastapi.tiangolo.com/) and [Redis](https://redis.io/).  If you find this useful, consider donating to [Mlomb](https://countapi.xyz/#donate), the creator of countapi.xyz 

## Documentation

Thanks to FastAPI there is swagger/OpenAPI doc endpoints included automatically and after deployment will be available at /docs and /redoc
```
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── conf
│   │   ├── __init__.py
│   │   └── config.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_main.py
│   └── main.py
├── .dockerignore
├── requirements.txt
└──  docker-compose.yml
```

## Deployment

First clone the repo locally 

``` git clone https://github.com/philip306/countapi.git ```

Install the prerequisites:

```pip install -r /requirements.txt```

Update config.py to point to your redis host/ip

```redishost: str = 'redis'```

Start Uvicorn:

```uvicorn app.main:app --port 8000```

Navigate to http://127.0.0.1:8000 in a browser

### Docker

First clone the repo locally 

``` git clone https://github.com/philip306/countapi.git ```

Update config.py to point to your redis host/ip

```redishost: str = 'redis'```

From within the count api directory build the docker image

```docker build -t countapi:0.1 .```

Run the image you just created

```docker run -p 8000:8000 --detach --name countapi countapi:0.1```

Navigate to http://127.0.0.1:8000 in a browser

### Docker Compose

Using ```docker-compose``` will use the deployment outlined in docker-compose.yml which will deploy a second container with a standard redis image

First clone the repo locally 

``` git clone https://github.com/philip306/countapi.git ```

From within the count api directory build the docker image

```docker build -t countapi:0.1 .```

Launch two separate containers with a redis image and the countapi image you just created

```docker-compose up```

Navigate to http://127.0.0.1:8000 in a browser

### AWS Lambda and Elasticache

_Coming soon_

## Testing

```pytest``` will execute the tests outlined in tests/test_main.py.  Currently very low coverage.

## Known Issues
Currently there is no TTL set on the keys, so the key will exist indefinitely.  You can clean them up manually if needed with redis-cli> flushdb
