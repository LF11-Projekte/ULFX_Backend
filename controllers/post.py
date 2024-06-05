from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from models import post, follow

PostRouter = APIRouter()


class Post(BaseModel):
    thumbnail: str
    teaser: str
    title: str
    content: str


class PutPost(BaseModel):
    thumbnail: str | None = None
    teaser: str | None = None
    title: str | None = None
    content: str | None = None


@PostRouter.post("/")
def get_newest_post(post_data: Post, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    post_id = post.create(user_id, post_data.thumbnail, post_data.teaser, post_data.title, post_data.content)

    return {"id": post_id}


@PostRouter.put("/:id")
def get_newest_post(post_data: PutPost, post_id: int, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    post.update(user_id, post_id, post_data.thumbnail, post_data.teaser, post_data.title, post_data.content)

    return 200


@PostRouter.get("/newest")
def get_newest_post(request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    return post.get_newest()


@PostRouter.get("/byId/:id")
def get_post_by_id(post_id: int, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    if not post_id:
        return HTTPException(status_code=404)

    return post.get_by_id(post_id)


@PostRouter.get("/followed")
def get_post_of_followed(request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    creators = []

    for x in follow.get_follower(user_id):
        if x.get("follower"):
            creators.append(x.get("follower"))

    return post.get_by_creators(creators)
