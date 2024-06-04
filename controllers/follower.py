from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from models import follow

FollowerRouter = APIRouter()


@FollowerRouter.get("/ofUser/:id")
def get_followers_of_user(user_id: int, request: Request):
    if not request.session.get("token"):
        return HTTPException(403)

    response = follow.get_follower(user_id)
    print(response)
    return {"followers": 0 if not response else len(response)}


class Follow(BaseModel):
    user_id: int


@FollowerRouter.post("/follow/:id")
def get_followers_of_user(follow_id: int, request: Request):
    if not request.session.get("token"):
        return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    if not user_id:
        return {"failed"}

    follow.follow(user_id, follow_id)
    return {"success"}


@FollowerRouter.post("/unfollow/:id")
def get_followers_of_user(follow_id: int, request: Request):
    if not request.session.get("token"):
        return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    if not user_id:
        return {"failed"}

    follow.unfollow(user_id, follow_id)
    return {"success"}

