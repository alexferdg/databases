# Entry point for the FastAPI
import socket
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from routes_crud import router as movie_router
import os
from dotenv import dotenv_values
from pymongo import MongoClient


# Environment variables
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
env_file_path = os.path.join(parent_dir, ".env")
config = dotenv_values(env_file_path)

# Application
app = FastAPI()

@asynccontextmanager
async def mongodb_lifespan(app: FastAPI):
    # Initialize the MongoDB client
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

    yield  # Yield control back to FastAPI until shutdown

    # Close the MongoDB connection
    app.mongodb_client.close()
    print("MongoDB connection closed.")

# app.router.lifespan_context = mongodb_lifespan(app)
app = FastAPI(lifespan = mongodb_lifespan) # Assign the lifespan context manager to the app

# Register the /movie endpoints
app.include_router(movie_router, tags=["movies"], prefix = "/movie")

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except socket.error as e:
            print(f"Port {port} is already in use.")
            return False

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    if check_port(host, port):
        uvicorn.run("movie_crud_fastapi:app", host=host, port=8000, reload=True)

# http://localhost:8000/docs API documentation page, which has been automatically created by FastAPI and Swagger