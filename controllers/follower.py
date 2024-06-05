from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from models import follow

FollowerRouter = APIRouter()


@FollowerRouter.get("/ofUser/:id")
def get_followers_of_user(user_id: int, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    response = follow.get_follower(user_id)
    print(response)
    return {"followers": 0 if not response else len(response)}


class Follow(BaseModel):
    user_id: int


@FollowerRouter.post("/follow/:id")
def get_followers_of_user(follow_id: int, request: Request, test_user_id: int = -1):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")

    if test_user_id != -1:
        user_id = test_user_id

    if not user_id or user_id < 0:
        return HTTPException(400)

    follow.follow(user_id, follow_id)
    return {"success"}


@FollowerRouter.post("/unfollow/:id")
def get_followers_of_user(follow_id: int, request: Request, test_user_id: int = -1):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")

    if test_user_id != -1:
        user_id = test_user_id

    if not user_id or user_id < 0:
        return HTTPException(400)

    follow.unfollow(user_id, follow_id)
    return {"success"}

