from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from models import comments

CommentsRouter = APIRouter()


@CommentsRouter.get("/ofPost/:id")
def get_comments_of_post(post_id: int, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    response = []

    for comment in comments.get_comments_of_post(post_id):
        subcomments = comments.get_comments_of_comment(comment.get("rowid"))
        response.append({"comment": comment,
                        "subcomments": subcomments})

    return response


@CommentsRouter.post("/post/:id")
def comment_post(post_id: int, comment_data: comments.PostCommentModel, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    if not user_id:
        return HTTPException(403)

    comments.add_comment(user_id, post_id, comment_data.content, 1)

    return "success"


@CommentsRouter.post("/comment/:id")
def comment_post(comment_id: int, comment_data: comments.PostCommentModel, request: Request):
    #if not request.session.get("token"):
    #   return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    if not user_id:
        return HTTPException(403)

    comments.add_comment(user_id, comment_id, comment_data.content, 0)

    return "success"


@CommentsRouter.put("/:id")
def comment_post(comment_id: int, comment_data: comments.PostCommentModel, request: Request):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    user_id = 1

    if not user_id:
        return HTTPException(403)

    comments.edit_comment(user_id, comment_id, comment_data.content)

    return "success"
