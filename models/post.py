import sqlite3
from pydantic import BaseModel
from utils import dict_factory


class Post(BaseModel):
    id: int
    creator: int
    thumbnail: str
    teaser: str
    title: str
    content: str
    created_at: str
    updated_at: str


class PostPost(BaseModel):
    thumbnail: str
    teaser: str
    title: str
    content: str


class PutPost(BaseModel):
    thumbnail: str | None = None
    teaser: str | None = None
    title: str | None = None
    content: str | None = None


def initialise():
    conn = sqlite3.connect('ulfx.db')
    conn.execute("CREATE TABLE IF NOT EXISTS post(" +
                 "creator INT NOT NULL," +
                 "thumbnail VARCHAR(255) NOT NULL," +
                 "teaser TEXT(300) NOT NULL," +
                 "title TEXT(50) NOT NULL," +
                 "content LONGTEXT NOT NULL," +
                 "created_at DATETIME NOT NULL," +
                 "updated_at DATETIME NOT NULL," +
                 "FOREIGN KEY (creator) REFERENCES User(rowid)" + ")"
                 )
    conn.close()


# return: post_id:int
def create(creator: int, thumbnail: str, teaser: str, title: str, content: str):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute(
        "INSERT INTO post (creator, thumbnail, teaser, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
        [creator, thumbnail, teaser, title, content])
    post_id = rs.lastrowid

    conn.commit()
    conn.close()
    return post_id


def update(creator: int, post_id: int, thumbnail: str = None, teaser: str = None, title: str = None, content: str = None):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    what = []
    params = []

    if thumbnail:
        what.append("thumbnail=?")
        params.append(thumbnail)

    if teaser:
        what.append("teaser=?")
        params.append(teaser)

    if title:
        what.append("title=?")
        params.append(title)

    if content:
        what.append("content=?")
        params.append(content)

    if len(what) > 0:
        what.append("updated_at=datetime('now')")
        params.append(post_id)
        params.append(creator)
        cursor.execute(f"UPDATE post SET {','.join(what)} WHERE rowid=? AND creator=?", params)

    conn.commit()
    conn.close()
    return post_id


# return: [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_newest(limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post ORDER BY created_at DESC LIMIT ?", [limit])
    data = rs.fetchall()

    conn.close()
    return data


# return [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_by_creator(creator: int, limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post WHERE creator=? ORDER BY created_at DESC LIMIT ?", [creator, limit])
    data = rs.fetchall()

    conn.close()
    return data


# return [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_by_creators(creators: list, limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    creators_list = []
    for creator in creators:
        if not type(creator) is int:
            continue
        creators_list.append(str(creator))

    rs = cursor.execute(f"SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post WHERE creator IN ({','.join(creators_list)}) ORDER BY created_at DESC LIMIT ?", [limit])
    data = rs.fetchall()

    conn.close()
    return data


# return (rowid,creator,thumbnail,teaser,title,content,created_at,updated_at)
def get_by_id(post_id: int):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post WHERE rowid=?", [post_id])
    data = rs.fetchone()

    conn.close()
    return data
