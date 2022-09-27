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
$ sudo docker-compose build web
$ docker-compose up -d
```

# Cheatsheet
1. Enter container - `docker exec -it <container_id> sh`
2. Connect to psql - `psql -U pug`
3. Connect to the database - `\c pug`
4. Show tables - `\dt`

#  Documentation
## Get courts sorted by distance from given coordinates with pagination
method = `GET`  
api_path = `api/v1/court/`
### Query parameters:  
`page`, `page_size` = optional, pagination info  
`lat`, `lon` = optional, user coordinates from which distance to the court is calculated    
`order_by`, `reverse` = optional, ordering info   

exemplary_api_path = `api/v1/court/?page=1&page_size=10&lat=56&lon=16.8&order_by=distance&reverse=True`

Note: If `lat` or `lon` parameters are not included, the `distance` parameter is set to `-1`.  

Extra parameters in response:
```
    "distance": 222.78,
    "rating": 5.8,
    "ratings_number": 1
```

## Get specific court
api_path = `/api/v1/court/<id>/`  
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
        "lightning": false,
        "type": "Indoor",
        "public": false,
        "rim_type": "Higher"
    }
}
```

## Get court details choices
### Surface
api_path = `/api/v1/surface`  
method = `GET`

### Rim type
api_path = `/api/v1/rim`  
method = `GET`

### Court type
api_path = `/api/v1/type`  
method = `GET`


## Insert timeframe
api_path = `/api/v1/timeframe/`  
method = `POST`
body:
```
{
    "player_nick": "pietrus",
    "start": 1663164000,
    "end": 1663171200,
    "court": 1
}
```

## Get playing timeframes frequency in specific range
api_path = `/api/v1/court/<court_id>/timeframes`  
method = `GET`  
query_params = `start` and `end` (both unix timestamps)  
exemplary_api_path = `/api/v1/court/1/timeframes/?start=1662393600&end=1662400800`
response:
```
{
    "frequency": {
        "09/05/2022, 16:00": 0, (it means that in range 16:00 - 16:30 there will 0 players on specific court)
        "09/05/2022, 16:30": 0,
        "09/05/2022, 17:00": 0,
        "09/05/2022, 17:30": 0
    }
}

```

## Insert rating
api_path = `/api/v1/rating/`
method = `POST`
body:
```
{
    "stars": 5.0,
    "court": 1
}
```
