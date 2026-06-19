from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
from app.routers import rpg_lore
from app.routers import map_regions
from fastapi.staticfiles import StaticFiles
from app.routers import rpg_notes
from app.routers import rpg_timeline
from app.routers import rpg_lore_relations
from app.routers import (
    rpg_timeline_categories,
)
from app.routers import rpg_factions
from app.routers import region_places
from app.routers import region_scenes
from app.routers import scene_locations

# ✅ WEBSOCKETS
from app.websockets.rpg_ws import router as ws_router
from app.websockets.notifications import router as ws_notifications_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# HTTP
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
app.include_router(rpg_lore.router)
app.include_router(map_regions.router)
app.include_router(rpg_notes.router)
app.include_router(rpg_timeline.router)
app.include_router(rpg_lore_relations.router)
app.include_router(rpg_timeline_categories.router)
app.include_router(rpg_factions.router)
app.include_router(region_places.router)
app.include_router(region_scenes.router)
app.include_router(scene_locations.router)
# 🔥 WS
app.include_router(ws_router)
app.include_router(ws_notifications_router)

@app.get("/")
def root():
    return {"status": "API online"}






