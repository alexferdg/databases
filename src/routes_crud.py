# Endpoints implementation
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import MovieModel, MovieUpdateModel
from pymongo.errors import DuplicateKeyError

router = APIRouter()

# POST /movie
@router.post("/", response_description = "Create a new Movie", status_code = status.HTTP_201_CREATED, response_model = MovieModel)
def create_movie(request: Request, movie: MovieModel = Body(...)):
    try:
        movie_data = jsonable_encoder(movie)
        new_movie = request.app.database["movies"].insert_one(movie_data)
        created_movie = request.app.database["movies"].find_one(
            {"_id": new_movie.inserted_id}
        )
        return created_movie
    except DuplicateKeyError:
        raise HTTPException(status_code = 409, detail = "A movie with the same ID already exits")

# GET /movie
@router.get("/", response_description = "List all movies", response_model = List[MovieModel])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies

# GET/movie/{id}
@router.get("/{id}", response_description="Get a single movie by id", response_model=MovieModel)
def find_movie(id: str, request: Request):
    if (movie := request.app.database["movies"].find_one({"id": id})) is not None:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

# PUT /movie/{id}
@router.put("/{id}", response_description="Update a movie", response_model=MovieModel)
def update_movie(id: str, request: Request, movie: MovieUpdateModel = Body(...)):
    movie_data = {k: v for k, v in movie.model_dump().items() if v is not None}
    if len(movie_data) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"_id": id}, {"$set": movie_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

    if (
        existing_movie := request.app.database["movies"].find_one({"_id": id})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

# DELETE /movie/{id}
@router.delete("/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.database["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

