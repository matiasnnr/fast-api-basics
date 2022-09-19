# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel  # allow us to create models
from pydantic import Field  # allow us to validate Models attributes

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str

    # inside Location class we create Config to set default values when we see the documentation in swagger or redoc
    class Config:
        schema_extra = {
            "example": {
                "city": "Puerto Montt",
                "state": "Décima",
                "country": "Chile",
            },
        }


class Person(BaseModel):  # (BaseModel) -> extends from BaseModel
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Matías"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Nunez"
    )
    age: int = Field(
        ...,
        gt=0,
        lt=115,
        example=28
    )
    # = None (null) will be the default value in case that we don't receive the hair_color argument.
    hair_color: Optional[HairColor] = Field(
        default=None,
        example="red"
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False
    )

    # inside Person class we create Config to set default values when we see the documentation in swagger or redoc
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Mati",
    #             "last_name": "Nunez",
    #             "age": 28,
    #             "hair_color": "black",
    #             "is_married": False
    #         },
    #     }


@app.get("/")  # this is a path operation decorator
def home():
    return {"Hello": "World"}


@app.get("/twitter/{id}/details")  # {id} is a path parameter
def twitter(id):
    text = f"twitter id {id} text"
    return {"twitter": text}


@app.post("/person/new")  # Request and response body
# (...): this means that this person Body is always required
def create_person(person: Person = Body(...)):
    return person

# If we have two endpoints with the same path then Python will select the first one from top to bottom

# Validations


@app.get('/person/detail')
def show_person(
    # default Query parameter is (None) null
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Nicolás"
    ),
    # default Query parameter is required (...)
    age: str = Query(
        ...,  # is required (...)
        title="Person Age",
        description="This is the person age. It's required",
        example=28
    )
):
    return {name: age}

# Validations: Path Parameters


@app.get('/person/detail/{person_id}')
def show_person_by_id(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Detail",
        description="This is the person detail.",
        example=77
    )
):
    return {person_id: 'It exists!'}

# Validations: Request Body


@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person id",
        gt=0,
        example=78
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    print(person_id)
    result = person.dict()  # convert this json to a dictionary
    # we're combining person + location in only one dictionary
    # otherwise we can use (return person.dict() & location.dict())
    # but Fast API still doesn't support this syntax
    result.update(location.dict())
    return result
