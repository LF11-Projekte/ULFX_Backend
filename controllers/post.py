from fastapi import APIRouter, Request, HTTPException
from models import post, follow
from models.post import Post

PostRouter = APIRouter()


@PostRouter.post("/")
def create_post(post_data: post.PostPost, request: Request, test_user_id: int = -1):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")

    if test_user_id != -1:
        user_id = test_user_id

    if not user_id or user_id < 0:
        return HTTPException(400)

    post_id = post.create(user_id, post_data.thumbnail, post_data.teaser, post_data.title, post_data.content)

    return {"id": post_id}


@PostRouter.put("/:id")
def edit_post(post_data: post.PutPost, post_id: int, request: Request, test_user_id: int = -1):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")

    if test_user_id != -1:
        user_id = test_user_id

    if not user_id or user_id < 0:
        return HTTPException(400)

    post.update(user_id, post_id, post_data.thumbnail, post_data.teaser, post_data.title, post_data.content)

    return 200


@PostRouter.get("/newest")
def get_newest_post(request: Request) -> list[post.Post]:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    response = []
    for x in post.get_newest():
        response.append(post.Post(
            id=x.get("rowid"),
            creator=x.get("creator"),
            thumbnail=x.get("thumbnail"),
            teaser=x.get("teaser"),
            title=x.get("title"),
            content=x.get("content"),
            created_at=x.get("created_at"),
            updated_at=x.get("updated_at")
        ))
    return response


@PostRouter.get("/byId/:id")
def get_post_by_id(post_id: int, request: Request) -> Post:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    if not post_id:
        return HTTPException(status_code=404)

    x = post.get_by_id(post_id)

    return post.Post(
        id=x.get("rowid"),
        creator=x.get("creator"),
        thumbnail=x.get("thumbnail"),
        teaser=x.get("teaser"),
        title=x.get("title"),
        content=x.get("content"),
        created_at=x.get("created_at"),
        updated_at=x.get("updated_at")
    )


@PostRouter.get("/followed")
def get_post_of_followed(request: Request, test_user_id: int = -1) -> list[post.Post]:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")

    if test_user_id != -1:
        user_id = test_user_id

    if not user_id or user_id < 0:
        return HTTPException(400)

    creators = []

    for x in follow.get_follower(user_id):
        if x.get("follower"):
            creators.append(x.get("follower"))

    response = []

    for x in post.get_by_creators(creators):
        response.append(post.Post(
            id=x.get("rowid"),
            creator=x.get("creator"),
            thumbnail=x.get("thumbnail"),
            teaser=x.get("teaser"),
            title=x.get("title"),
            content=x.get("content"),
            created_at=x.get("created_at"),
            updated_at=x.get("updated_at")
        ))
    return response


@PostRouter.get("/byUserId/:id")
def get_post_of_user(user_id: int, request: Request) -> list[post.Post]:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    response = []

    for x in post.get_by_creator(user_id):
        response.append(post.Post(
            id=x.get("rowid"),
            creator=x.get("creator"),
            thumbnail=x.get("thumbnail"),
            teaser=x.get("teaser"),
            title=x.get("title"),
            content=x.get("content"),
            created_at=x.get("created_at"),
            updated_at=x.get("updated_at")
        ))
    return response

