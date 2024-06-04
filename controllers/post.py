from fastapi import APIRouter, Request, HTTPException
from models import post, follow

PostRouter = APIRouter()


@PostRouter.get("/newest")
def get_newest_post(request: Request):
    if not request.session.get("token"):
        return HTTPException(403)

    return post.get_newest()


@PostRouter.get("/byId/:id")
def get_post_by_id(post_id: int, request: Request):
    if not request.session.get("token"):
       return HTTPException(403)

    if not post_id:
        return HTTPException(status_code=404)

    return post.get_by_id(post_id)


@PostRouter.get("/followed")
def get_post_of_followed(request: Request):
    if not request.session.get("token"):
       return HTTPException(403)

    user_id = request.session.get("user_id")

    creators = []

    for x in follow.get_follower(user_id):
        if x.get("follower"):
            creators.append(x.get("follower"))

    return post.get_by_creators(creators)
