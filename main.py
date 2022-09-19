# Python
from typing import Optional, List
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

    class Config:
        schema_extra = {
            "example": {
                "city": "Puerto Montt",
                "state": "Décima",
                "country": "Chile",
            },
        }


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(
        default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)


class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="12345678"
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfully!")


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home Title"  # title for swagger
)
def home():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"Hello": "World"}

# Request and Response Body


@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in App"
)
def create_person(person: Person = Body(...)):
    """
    _This path operation creates a person in the application and save the information in database._

    Args:
        person (Person): _description_. Defaults to Body(...).

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first_name, last_name, age, hair_color, is_married and password

    Returns:
        _Person Model_: _contains first_name, last_name, age, hair_color, is_married and password_
    """
    return person

# Validaciones: Query Parameters


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocío"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
    )
):
    """_summary_

    Args:
        name (Optional[str]): _description_. Defaults to Query( None, min_length=1, max_length=50, title="Person Name", description="This is the person name. It's between 1 and 50 characters", example="Rocío" ).
        age (str): _description_. Defaults to Query( ..., title="Person Age", description="This is the person age. It's required", example=25 ).

    Returns:
        _type_: _description_
    """
    return {name: age}

# Validaciones: Path Parameters


persons = [1, 2, 3, 4, 5]


@app.get(
    path="/person/detail/{person_id}",
    tags=["Persons"]
)
def show_person_by_id(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
    )
):
    """_summary_

    Args:
        person_id (int): _description_. Defaults to Path( ..., gt=0, example=123 ).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if (person_id not in persons):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body


@app.put(
    path="/person/{person_id}",
    tags=["Persons"]
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    """_summary_

    Args:
        person_id (int): _description_. Defaults to Path( ..., title="Person ID", description="This is the person ID", gt=0, example=123 ).
        person (Person): _description_. Defaults to Body(...).
        location (Location): _description_. Defaults to Body(...).

    Returns:
        _type_: _description_
    """
    print(person_id)
    results = person.dict()
    results.update(location.dict())
    return results

# Forms


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Auth"]
)
def login(username: str = Form(...), password: str = Form(...)):
    """_summary_

    Args:
        username (str): _description_. Defaults to Form(...).
        password (str): _description_. Defaults to Form(...).

    Returns:
        _type_: _description_
    """
    return LoginOut(username=username)

# Cookies and Headers Parameters


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(
        ...,
    ),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None, example="me"),
    ads: Optional[str] = Cookie(default=None, example="Cookies values")
):
    """_summary_

    Args:
        first_name (str): _description_. Defaults to Form( ..., max_length=20, min_length=1, ).
        last_name (str): _description_. Defaults to Form( ..., max_length=20, min_length=1, ).
        email (EmailStr): _description_. Defaults to Form( ..., ).
        message (str): _description_. Defaults to Form( ..., min_length=20, ).
        user_agent[str]): _description_. Defaults to Header(default=None, example="me").
        ads[str]): _description_. Defaults to Cookie(default=None, example="Cookies values").

    Returns:
        _type_: _description_
    """
    print(ads)
    return user_agent

# Files


@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    """_summary_

    Args:
        image (UploadFile): _description_. Defaults to File(...).

    Returns:
        _type_: _description_
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }


@app.post(
    path='/post-multiple-images',
    tags=["Files"]
)
def post_multiple_images(
    images: List[UploadFile] = File(...)
):
    """_summary_

    Args:
        images (List[UploadFile]): _description_. Defaults to File(...).

    Returns:
        _type_: _description_
    """
    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    } for image in images]
    print(f'info_images {info_images}')
    return info_images
