import sqlite3
from pydantic import BaseModel
from utils import dict_factory


class PostCommentModel(BaseModel):
    content: str


def initialise():
    conn = sqlite3.connect('ulfx.db')
    conn.execute("CREATE TABLE IF NOT EXISTS comment(" +
                 "creator INT," +
                 "reference INT," +
                 "content TEXT," +
                 "isPostComment INT," +
                 "created_at DATETIME NOT NULL," +
                 "updated_at DATETIME NOT NULL," +
                 "FOREIGN KEY(creator) REFERENCES user(rowid)" +
                 ")")
    conn.commit()
    conn.close()


def add_comment(creator, reference, content, is_post_comment):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO comment (creator,reference,content,isPostComment,created_at,updated_at) VALUES (?,?,?,?, datetime('now'), datetime('now'))", (creator, reference, content, is_post_comment))
    comment_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return comment_id


def edit_comment(creator, comment_id, content):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE comment SET content=? WHERE creator=? AND rowid=?", (content, creator, comment_id))

    conn.commit()
    conn.close()
    return "success"


def delete_comment(creator, comment_id):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM comment WHERE rowid=? AND creator=?", (comment_id, creator))
    conn.commit()
    conn.close()
    return "success"


def get_comments_of_post(post_id):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute("SELECT rowid,* FROM comment WHERE reference=? AND isPostComment=1", (post_id,))
    rs = cursor.fetchall()

    conn.close()
    return rs


def get_comments_of_comment(comment_id):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute("SELECT rowid,* FROM comment WHERE reference=? AND isPostComment=0", (comment_id,))
    rs = cursor.fetchall()

    conn.close()
    return rs
