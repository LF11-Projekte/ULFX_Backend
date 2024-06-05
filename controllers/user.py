from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from models import user

UserRouter = APIRouter()


class Me(BaseModel):
    displayname: str | None = None
    description: str | None = None


@UserRouter.get("/me")
def get_user(request: Request, token: str = None):
    if not token:
        if not request.session.get("token"):
            return HTTPException(403)
        token = request.session.get("token")


    if not token:
        return HTTPException(403)

    result = user.get_me_data(token)
    return result if result else HTTPException(400)


@UserRouter.put("/me/")
def get_user(request: Request, me: Me, token: str = None):
    if not token:
        if not request.session.get("token"):
            return HTTPException(403)
        token = request.session.get("token")

    status = []

    if me.description:
        status.append(user.update_me_description(me.description, token))

    if me.displayname:
        status.append(user.update_me_displayname(me.displayname, token))

    problems = False

    for stat in status:
        if stat != 200: problems = True

    return 200 if not problems else HTTPException(500)


@UserRouter.get("/byId/:id")
def get_user_by_id(user_id: int, request: Request, token: str = None):
    if not token:
        if not request.session.get("token"):
            return HTTPException(403)
        token = request.session.get("token")

    aduser = user.get_aduser(user_id)
    if aduser == -1:
        return HTTPException(404)
    aduser = aduser.get("aduser")

    response = user.get_user_data(aduser, token)
    response["id"] = user_id
    return response
