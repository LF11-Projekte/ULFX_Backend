from fastapi import APIRouter, Request, HTTPException
from models import post, view

PostRouter = APIRouter()


@PostRouter.get("/newest")
def get_newest_post(request: Request):
    newest_post = post.get_newest()

    response = []
    for x in newest_post:
        response.append({
            "id": x[0],
            "title": x[4],
            "previewPicture": x[2],
            "previewText": x[3],
            "lastEditDate": x[7],
            "creationDate": x[6],
            "views": view.get_viewers(x[0])[0],
            "user": x[1],
            "content": x[5],
        })

    return response


@PostRouter.get("/byId/:id")
def get_post_by_id(post_id: int, request: Request):
    if not post_id:
        return HTTPException(status_code=404)

    result = post.get_by_id(post_id)
    response = {
        "id": result[0][0],
        "title": result[0][4],
        "previewPicture": result[0][2],
        "previewText": result[0][3],
        "lastEditDate": result[0][7],
        "creationDate": result[0][6],
        "views": view.get_viewers(result[0][0])[0],
        "user": result[0][1],
        "content": result[0][5],
    }
    return response
