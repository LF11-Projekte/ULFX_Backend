from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from models import user

UserRouter = APIRouter()


class Me(BaseModel):
    user_id: int | None = None
    adname: str | None = None
    displayname: str | None = None
    description: str | None = None
    profilePicture: str | None = None


@UserRouter.get("/me")
def get_user(request: Request, token: str = None) -> Me:
    if not token:
        if not request.session.get("token"):
            return HTTPException(403)
        token = request.session.get("token")

    result = user.get_me_data(token)

    if not result:
        return HTTPException(403)

    print(result)

    return Me(
        user_id=request.session.get("user_id"),
        adname=result.get("adName"),
        displayname=result.get("displayName"),
        description=result.get("description"),
    )


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
