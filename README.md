# Installation 
soon
# Deployment
soon 
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