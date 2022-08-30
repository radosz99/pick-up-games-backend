# API link
```
https://backend.matcher.pl/api/v1/
```

# Deployment
1. Clone project and get to root directory;
```
$ git clone https://github.com/radosz99/pick-up-games-backend.git && cd pick-up-games-backend
```
2. Run `docker-compose` as a daemon:
```
$ docker-compose up -d
```
3. Enter application container:
```
$ docker exec -it <container_id> sh
```
4. Make migrations:
```
$ poetry run python manage.py migrate
```

# Cheatsheet
1. Enter container - `docker exec -it <container_id> sh`
2. Connect to psql - `psql -U pug`
3. Connect to the database - `\c pug`
4. Show tables - `\dt`
#  Documentation
## Get courts
api_path = `/api/v1/court`  
method = `GET`

## Get specific court
api_path = `/api/v1/court/<id>`  
method = `GET`

## Create court object
api_path = `/api/v1/court/` (trailing slash is important)  
method = `POST`  
body:
```
{
    "name": "xd",
    "address": {
        "latitude": 56,
        "longitude": 17,
        "country": "Poland",
        "city": "Wroclaw",
        "postal_code": "53-533",
        "street_name": "Zielinskiego",
        "street_number": "49/2"
    },
    "details": {
        "surface": "Dirt",
        "courts_number": 2,
        "hoops_number": 4,
        "lightning": false
    }
}
```

## Get surface types
api_path = `/api/v1/surface`  
method = `GET`


