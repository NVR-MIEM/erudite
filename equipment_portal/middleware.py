import os
import logging
from fastapi import FastAPI, Request, HTTPException, Response


DATABASE_URI = os.environ.get("DATABASE_URI")


async def authorization(request: Request, call_next):
    api_key = request.headers.get("key", "")

    response = await check_jwt_token_and_key(api_key)
    if not response.status_code == 200:
        return response

    response = await call_next(request)
    return response


async def check_jwt_token_and_key(key: str):
    return Response("delete in prod", status_code=200)

    if key:
        try:
            conn = await asyncpg.connect(DATABASE_URI)
            user = await conn.fetchrow("SELECT * FROM users WHERE api_key = $1", key)
            await conn.close()
            if not user:
                return Response(f"User not found", status_code=401)
            return Response("ok", status_code=200)
        except Exception as exp:
            logging.error(exp)
            return Response(f"{exp}", status_code=401)
    return Response("Invalid token and key", status_code=401)
