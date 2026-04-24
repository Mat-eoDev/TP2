import os

import mysql.connector
from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def get_conn() -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(
        host=_env("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=_env("MYSQL_DATABASE"),
        user=_env("MYSQL_USER"),
        password=_env("MYSQL_PASSWORD"),
    )

def get_mongo():
    uri = _env("MONGO_URI")
    return MongoClient(uri, serverSelectionTimeoutMS=3000)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users")
def get_users():
    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs")
        records = cursor.fetchall()
        return {"count": len(records), "utilisateurs": records}
    finally:
        conn.close()


@app.get("/posts")
def get_posts():
    client = get_mongo()
    try:
        db_name = _env("MONGO_DB")
        posts = list(client[db_name]["posts"].find({}, {"_id": 0}))
        return {"count": len(posts), "posts": posts}
    finally:
        client.close()


@app.get("/health")
def health():
    users = get_users()
    posts = get_posts()
    if users.get("count") is None or posts.get("count") is None:
        raise RuntimeError("Unhealthy")
    return {"ok": True, "users": users["count"], "posts": posts["count"]}
