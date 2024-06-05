from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from models import comments

CommentsRouter = APIRouter()


@CommentsRouter.get("/ofPost/:id")
def get_comments_of_post(post_id: int, request: Request) -> list [comments.PostCommentsModel]:
    #if not request.session.get("token"):
    #    return HTTPException(403)

    response = []

    for comment in comments.get_comments_of_post(post_id):
        subcomments = []

        for x in comments.get_comments_of_comment(comment.get("rowid")):
            subcomments.append(comments.CommentModel(
                id=x.get("rowid"),
                creator=x.get("creator"),
                reference=x.get("reference"),
                content=x.get("content"),
                isPostComment=x.get("isPostComment"),
                created_at=x.get("created_at"),
                updated_at=x.get("updated_at"),
            ))

        response.append(comments.PostCommentsModel(
            comment=comments.CommentModel(
                id=comment.get("rowid"),
                creator=comment.get("creator"),
                reference=comment.get("reference"),
                content=comment.get("content"),
                isPostComment=comment.get("isPostComment"),
                created_at=comment.get("created_at"),
                updated_at=comment.get("updated_at"),
            ),
            subcomment=subcomments
        ))

    return response


@CommentsRouter.post("/post/:id")
def comment_post(post_id: int, comment_data: comments.PostCommentModel, request: Request, test_user_id: int):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    if test_user_id:
        user_id = test_user_id

    if not user_id:
        return HTTPException(403)

    comments.add_comment(user_id, post_id, comment_data.content, 1)

    return "success"


@CommentsRouter.post("/comment/:id")
def comment_post(comment_id: int, comment_data: comments.PostCommentModel, request: Request, test_user_id: int):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    if test_user_id:
        user_id = test_user_id

    if not user_id:
        return HTTPException(403)

    comments.add_comment(user_id, comment_id, comment_data.content, 0)

    return "success"


@CommentsRouter.put("/:id")
def comment_post(comment_id: int, comment_data: comments.PostCommentModel, request: Request, test_user_id: int):
    #if not request.session.get("token"):
    #    return HTTPException(403)

    user_id = request.session.get("user_id")
    if test_user_id:
        user_id = test_user_id

    if not user_id:
        return HTTPException(403)

    comments.edit_comment(user_id, comment_id, comment_data.content)

    return "success"
