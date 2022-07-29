from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from euros import collect_duplicate_euro_numbers, common_euros_generator
from lotto import collect_duplicate_lotto_numbers, common_lotto_generator

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static/dist"), name="static")


@app.get("/")
async def root():
    return {"message": "I am Root"}


@app.get("/lotto")
def lotto_numbers():
    return collect_duplicate_lotto_numbers()


@app.get("/euros")
def euro_numbers():
    return collect_duplicate_euro_numbers()


@app.get("/generate-lotto")
def generate_lotto_numbers():
    return common_lotto_generator()


@app.get("/generate-euros")
def generate_euros_numbers():
    return common_euros_generator()
