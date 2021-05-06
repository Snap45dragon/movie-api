# movie-collections-api
A web application which allows people to create collections of movies they like. There are three parts to this:
- Users can register and authenticate with JWT token provided at first time.
- Post-login, the users can get a list of movies and its details.
- Post-login, the users can create collections and add movies to their collections, view, modify and delete them.

## Register a user
Request: 
```
POST http://localhost:8000/register/
```

Payload: 
```
{
  “username”: <desired username>,
  “password”: <desired password> 
}
```

Response:  
```
{  
  “access_token”: <Access Token>,  
  "refresh_token": <Refresh Token>  
}
```

## Refresh an expired token
Request: 
```
POST http://localhost:8000/register/refresh 
```

Payload:
```
{
  "refresh": <refresh token>
}
```

Response:
```
{
  "access_token": <access token>
}
```

## Get list of all the movies
Request:
```
GET http://localhost:8000/movies/
```

Response:
```
{
  “count”: <total number of movies>,
  “next”: <link for next page, if present>,
  “previous”: <link for previous page>,
  “data”: [
      {
  	“title”: <title of the movie>,
  	“description”: <a description of the movie>,
  	“genres”: <a comma separated list of genres, ifpresent>,
  	“uuid”: <a unique uuid for the movie>
      },
      ...
  ]
}
```

## Create a collection 
Request:
```
POST http://localhost:8000/collection/
```
Payload:
```
{
  “title”: “<Title of the collection>”,
  “description”: “<Description of the collection>”,
  “movies”: [
      {
        “title”: <title of the movie>,
        “description”: <description of the movie>,
        “genres”: <generes>,
        “uuid”: <uuid>
      }, 
      ...
  ]
}
```
Response:
```
{
  “collection_uuid”: <uuid of the collection item>
}
```

## View all collections 
Request:
```
GET http://localhost:8000/collection/
```
Response:
- If there are any collections
```
{
  “is_success”: True,
  “data”: {
    “collections”: [
      {
        “title”: “<Title of my collection>”,
        “uuid”: “<uuid of the collection name>”
        “description”: “My description ofthe collection.”
      },
      ...
    ],
    “favourite_genres”: “<My top 3 favorite genresbased on themovies I have added in my collections>.”
  }
}
```
- If there are no collections
```
{
  "error": "collections are empty"
}
```

## View a collection
Request:
```
GET http://localhost:8000/collection/<collection_uuid>/
```
Response:
- If collection exists
```
{
  “title”: <Title of the collection>,
  “description”: <Description of the collection>,
  “movies”: <Details of movies in my collection>
}
```
- If collection does not exist
```
{
    "error": "uuid does not exist"
}
```

## Update a collection
Request:
```
PUT http://localhost:8000/collection/<collection_uuid>/
```
Payload:
```
{
  “title”: <Optional updated title>,
  “description”: <Optional updated description>,
  “movies”: <Optional movie list to be updated>,
}
```
Response:
- If collection exists
```
{
  "is_success": true
}
```
- If collection does not exist
```
{
    "error": "uuid does not exist"
}
```

## Delete a collection
Request:
```
DELETE http://localhost:8000/collection/<collection_uuid>/
```
Response:
- If collection exists
```
{
  "is_success": true
}
```
- If collection does not exist
```
{
    "error": "uuid does not exist"
}
```

## Unauthorized access not allowed
For all the types of requests listed:
```
GET http://localhost:8000/movies/
POST http://localhost:8000/collection/
GET http://localhost:8000/collection/
GET http://localhost:8000/collection/<collection_uuid>/
PUT http://localhost:8000/collection/<collection_uuid>/
DELETE http://localhost:8000/collection/<collection_uuid>/
```
Unauthorised access will lead to following error:
```
{
    "detail": "Authentication credentials were not provided."
}
```














