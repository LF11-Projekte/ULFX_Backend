from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from models import user

UserRouter = APIRouter()


class Me(BaseModel):
    displayname: str | None = None
    description: str | None = None


@UserRouter.get("/me")
def get_user(request: Request):
    token = request.session.get("token")

    if not token:
        return HTTPException(403)

    result = user.get_me_data(token)
    return result if result else HTTPException(400)


@UserRouter.put("/me/")
def get_user(request: Request, me: Me):
    token = request.session.get("token")

    if not token:
        return HTTPException(403)

    status = []

    if me.description:
        status.append(user.update_me_description(me.description, token).status_code)

    if me.displayname:
        status.append(user.update_me_displayname(me.displayname, token).status_code)

    problems = False

    for stat in status:
        if stat != 200: problems = True

    return 200 if not problems else HTTPException(500)


@UserRouter.get("/byId/:id")
def get_user_by_id(user_id: int, request: Request):
    aduser = user.get_aduser(user_id)
    aduser = "d22jahnka"
    token = request.session.get("token")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZDIya3Jva2VyYWQiLCJhY2Nlc3NUb2tlbiI6IjMwMzY4YjRkLWYyZWEtNGFiMS05Mzc5LWU5NjRjOWExY2U5NiIsInJlZnJlc2hUb2tlbiI6ImI4OTM4NTBkLWJkYjUtNDFiYi1hZDdmLTI4ZjNmNDQ4OTNmMSIsImV4cGlyZXMiOjE3MTc0OTEyMjYxNDgsImlhdCI6MTcxNzQ4NzYyNn0.6hApSXZZMk-EeRkz8lFKi65s9m9ydcLlUuOwChFmBRA"
    response = user.get_user_data(aduser, token)
    response["id"] = user_id
    return response
