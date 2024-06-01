import sqlite3


def initialise():
    conn = sqlite3.connect('ulfx.db')
    conn.execute("CREATE TABLE IF NOT EXISTS user (" +
                 "aduser VARCHAR(255) PRIMARY KEY" +
                 ")")
    conn.close()


def get_id(aduser: str):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM user WHERE aduser=?", [aduser])
    rs = cursor.fetchone()
    if rs and len(rs) > 0:
        return rs[0]
    return -1


def create(aduser: str):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute("INSERT INTO user (aduser) VALUES (?)", [aduser])
    user_id = rs.lastrowid

    conn.commit()
    conn.close()
    return user_id
