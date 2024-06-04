import sqlite3
from utils import dict_factory


def search(aduser: str = None, title: str = None, teaser: str = None):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    response = {}

    if aduser:
        cursor.execute("SELECT rowid,* FROM user WHERE aduser LIKE ?", (f"%{aduser}%",))
        rs = cursor.fetchall()
        response['user'] = rs

    if title and teaser:
        cursor.execute("SELECT rowid,* FROM post WHERE title LIKE ? AND teaser LIKE ?", (f"%{title}%", f"%{teaser}%"))
        rs = cursor.fetchall()
        response['post'] = rs

    elif title:
        cursor.execute("SELECT rowid,* FROM post WHERE title LIKE ?", (f"%{title}%",))
        rs = cursor.fetchall()
        response['post'] = rs

    elif teaser:
        cursor.execute("SELECT rowid,* FROM post WHERE teaser LIKE ?", (f"%{teaser}%",))
        rs = cursor.fetchall()
        response['post'] = rs

    return response