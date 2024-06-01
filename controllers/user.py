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
