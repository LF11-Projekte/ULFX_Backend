import requests
import sqlite3
from config import USERMANAGER_URL
from utils import dict_factory


def initialise():
    conn = sqlite3.connect('ulfx.db')
    conn.execute("CREATE TABLE IF NOT EXISTS user (" +
                 "aduser VARCHAR(255) PRIMARY KEY" +
                 ")")
    conn.close()


# return user_id | -1
def get_id(aduser: str):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM user WHERE aduser=?", [aduser])
    rs = cursor.fetchone()
    if rs and len(rs) > 0:
        return rs
    return -1


# return aduser | -1
def get_aduser(user_id: int):
    conn = sqlite3.connect('ulfx.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT aduser FROM user WHERE rowid=?", [user_id])
    rs = cursor.fetchone()
    conn.close()
    if rs and len(rs) > 0:
        return rs
    return -1


# return user_id
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
