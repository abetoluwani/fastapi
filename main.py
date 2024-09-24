from urllib.request import Request
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from auth import *
app = FastAPI()

@app.get("/")
async def index():
    return {"Welcome To My Api"}
@app.post ("/register")
async def register(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = hash_password(user_info["password"]) # converting a plain text to hashed password
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        'status': 'success',
        "data" : f"Hello {new_user.username}, Please check your email and click on the link to confirm your email.",
    }


register_tortoise(
    app,
    db_url="sqlite:///db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)