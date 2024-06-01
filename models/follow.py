import sqlite3


def initialise():
    conn = sqlite3.connect('ulfx.db')
    conn.execute("CREATE TABLE IF NOT EXISTS follower(" +
                 "follower INT," +
                 "followed INT,"
                 "FOREIGN KEY(follower) REFERENCES user(rowid)," +
                 "FOREIGN KEY(followed) REFERENCES user(rowid)" +
                 ")")
    conn.commit()
    conn.close()


def follow(follower: int, followed: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM follower WHERE follower=? AND followed=?", [follower, followed])
    rs = cursor.fetchall()
    if not rs or (rs and rs[0][0] == 0):
        cursor.execute("INSERT INTO follower (follower,followed) VALUES (?,?)", [follower, followed])
        conn.commit()
    conn.close()


def unfollow(follower: int, followed: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM follower  WHERE follower=? AND followed=?", [follower, followed])
    conn.commit()
    conn.close()


def get_followed(follower: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()
    rs = cursor.execute("SELECT followed FROM follower WHERE follower=?", [follower])
    data = rs.fetchall()
    conn.commit()
    conn.close()
    return data


def get_follower(followed: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()
    rs = cursor.execute("SELECT follower FROM follower WHERE followed=?", [followed])
    data = rs.fetchall()
    conn.commit()
    conn.close()
    return data


# return: True/False
def do_follow(follower: int, followed: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM follower WHERE follower=? AND followed=?", [follower, followed])
    rs = cursor.fetchall()
    return False if (rs and rs[0][0] == 0) or not rs else True
