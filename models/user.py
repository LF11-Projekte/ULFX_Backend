import requests
import sqlite3
from config import USERMANAGER_URL


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


# return {description: str, profilePicture: str, privileges: int, id: int, adName: str, displayName: str}
def get_user_data(aduser: str, token: str):
    res = requests.get(f"{USERMANAGER_URL}/user/{aduser}", headers={"Authorization": f"Bearer {token}"})
    return res.json() if res.status_code == 200 else None


# return {description: str, profilePicture: str, privileges: int, id: int, adName: str, displayName: str}
def get_me_data(token: str):
    res = requests.get(f"{USERMANAGER_URL}/user/me", headers={"Authorization": f"Bearer {token}"})
    return res.json() if res.status_code == 200 else None


def update_me_displayname(displayname: str, token: str):
    res = requests.put(f"{USERMANAGER_URL}/user/me/displayname", headers={"Authorization": f"Bearer {token}",
                                                                          "Content-type": "application/json"},
                       json={"displayName": displayname})
    return res.status_code


def update_me_description(description: str, token: str):
    res = requests.put(f"{USERMANAGER_URL}/user/me/description", headers={"Authorization": f"Bearer {token}",
                                                                          "Content-type": "application/json"},
                       json={"description": description})
    return res.status_code
