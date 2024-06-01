import sqlite3


def initialise():
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS view(" +
                   "userId INT NOT NULL," +
                   "postId INT NOT NULL," +
                   "FOREIGN KEY(userId) REFERENCES user(rowid)," +
                   "FOREIGN KEY(postId) REFERENCES post(rowid)" +
                   ")"
                   )

    conn.commit()
    conn.close()


def view(user_id, post_id):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO view (userId, postId) VALUES (?,?)", [user_id, post_id])

    conn.commit()
    conn.close()


# return (viewers,)
def get_viewers(post_id: int):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    rs = cursor.execute("SELECT COUNT(*) FROM view WHERE postId = ?", [post_id])
    data = rs.fetchone()

    conn.close()
    return data


# return: [(post_id, viewers), ...]
def get_most_viewed_postIds(limit: int = 30):
    conn = sqlite3.connect('ulfx.db')
    cursor = conn.cursor()

    cursor.execute("SELECT postId, COUNT(*) AS post_count FROM view GROUP BY postId ORDER BY post_count DESC LIMIT ?", [limit])
    rs = cursor.fetchall()

    conn.close()
    return rs
