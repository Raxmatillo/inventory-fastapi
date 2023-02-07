from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://127.0.0.1:8000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-12099.c250.eu-central-1-1.ec2.cloud.redislabs.com",
    port=12099,
    password="FMiBgLWb19uxw1EAmNLwBHi3h43LOaiN",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return Product.all_pks()


def format(pk: str):
    product = Product.get(pk)


@app.post("/products")
def create(product: Product):
    return product.save()


@app.get("/")
async def root():
    return {"message": "Hello World"}