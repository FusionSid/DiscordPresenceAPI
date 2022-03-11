import os
import asyncio
import discord
from utils import Card
from dotenv import load_dotenv
from discord.ext import commands
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, RedirectResponse

load_dotenv()

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.all()
intents.presences = True
intents.members = True


client = commands.Bot(">", intents=intents)

app = FastAPI()


@client.event
async def on_ready():
    print("Bot is ready!")

@app.get("/api/image")
async def image(request : Request, user_id : int):
    main_guild = await client.fetch_guild(763348615233667082)
    try:
        user = await main_guild.fetch_member(user_id)
    except discord.errors.NotFound as err:
        if err.code == 10007:
            return {"error" : f"{err}", "fix" : "Make sure you are in the guild: https://discord.gg/p9GuT5hakm"}

        if err.code == 10013:
            return {"error" : f"{err}", "fix" : "Make sure user_id is correct"}

    card = Card(user)

    if user.activity is None:
        image = await card.status_image()
    else:
        image = await card.activity_image()
        
    return StreamingResponse(image, 200, media_type="image/png")


@app.get("/discord")
async def discord_server():
    return RedirectResponse("https://discord.gg/p9GuT5hakm")


@app.on_event("startup")
async def startup_event():
  asyncio.create_task(client.start(TOKEN))