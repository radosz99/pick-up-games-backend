# API url
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
$ sudo docker-compose up -d --build
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

### Query parameters:
`lat`, `lon` = optional, user coordinates from which distance to the court is calculated  

exemplary_api_path = `api/v1/court/7/?lat=56&lon=16.8`

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

## Get court images
api_path = `/api/v1/court/<court_id>/images`  
method = `GET`

## Insert image
TODO

## Get court details choices
api_path = `api/v1/court_details/choices`  
method = `GET`  
response:
```
{
    "rim_type": [
        "Higher",
        "Lower",
        "Normal",
        "Various"
    ],
    "court_type": [
        "Indoor",
        "Outdoor"
    ],
    "surface_type": [
        "Cement",
        "Concrete",
        "Dirt",
        "Grass",
        "Plastic",
        "Rubber",
        "Wood",
        "Other"
    ]
}
```

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

## Insert comment
api_path = `/api/v1/comment/`
method = `POST`
body:
```
{
    "content": "nice court",
    "court": 1
}
```

## Get comment for specific court with pagination
exemplary_api_path = `/api/v1/comment/?court_id=36&page=1&page_size=1`  
method = `GET`


## IP validation 
Two IP validation methods have been implemented and can be used together or separately. They are checking if model (which has `Court` object) has not been created with specific court from given IP either too many times (`AMOUNT` validation) or recently (`ELAPSED_TIME` validation).  

Can be used for:
- Rating, 
- Comment,
- Timeframe.

### By maximum amount
Using validation decorator:
```
@validate_ip(model=Rating, validation_type=ValidationType.AMOUNT, value=1)
```
Specific response can be returned:
```
{
    "detail": "IP validation not successful, total number (1) of Rating objects created in database from ip = 172.20.0.1 for court_id = 36 has exceeded or is equal to maximum allowed (1)",
    "exception": "TooManyRequestsFromIpException"
}
```
### By minimal elapsed time
Using validation decorator:
```
@validate_ip(model=Comment, validation_type=ValidationType.TIME_ELAPSED, value=timedelta(minutes=1))
```
Specific response can be returned:
```
{
    "detail": "IP validation not successful, last created Comment object from ip 172.20.0.1 for court_id = 36 had been created on 2022-09-28 12:43:03.714972+00:00, only 0:00:13.222064 time has elapsed till now (2022-09-28 12:43:16.937036+00:00) and minimum is = 0:01:00",
    "exception": "TooManyRequestsFromIpException"
}
```
