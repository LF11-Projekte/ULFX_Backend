import sqlite3


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


# return: [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_newest(limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post ORDER BY created_at DESC LIMIT ?", [limit])
    data = rs.fetchall()

    conn.close()
    return data


# return [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_by_creator(creator: int, limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post WHERE creator=? ORDER BY created_at DESC LIMIT ?", [creator, limit])
    data = rs.fetchall()

    conn.close()
    return data


# return [(rowid,creator,thumbnail,teaser,title,content,created_at,updated_at), ...]
def get_by_id(creator: int, limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute("SELECT rowid,creator,thumbnail,teaser,title,content,created_at,updated_at FROM post WHERE creator=? ORDER BY created_at DESC LIMIT ?", [creator, limit])
    data = rs.fetchall()

    conn.close()
    return data
