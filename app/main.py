from fastapi import FastAPI
from app.routers import auth
from app.routers import users
from app.routers import posts
from app.routers import rpg
from app.routers import rpg_turn
from app.routers import characters
from app.routers import rpg_chat
from app.routers import rpg_sheet_fields
from app.routers import character_sheets
from app.routers import notifications
from app.routers import search
from app.routers import feed

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(rpg.router)
app.include_router(rpg_turn.router)
app.include_router(characters.router)
app.include_router(rpg_chat.router)
app.include_router(rpg_sheet_fields.router)
app.include_router(character_sheets.router)
app.include_router(notifications.router)
app.include_router(search.router)
app.include_router(feed.router)










