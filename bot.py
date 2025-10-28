import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Load environment variables from .env file
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# ---- SPOTIFY SETUP ----
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Setup intents (needed for reading messages)
intents =  discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='nigga!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")

@bot.command()
async def hello(ctx):
    await ctx.send(f"👋 sup {ctx.author.mention} my nigga!")
    print(f"Send {ctx.author.name} a hello message")

@bot.command()
async def reco(ctx, genre: str, era: str):
    """Get song recommendations based on genre and era"""
    await ctx.send(f"🔍 Searching for **{genre} songs from the {era}**...")
    
    # Combine genre + era into search query
    query = f"{genre} {era}"
    results = sp.search(q=query, type='track', limit=10)

    tracks = results['tracks']['items']
    if not tracks:
        await ctx.send("😔 No songs found. Try a different genre or era.")
        return

    message = f"🎶 **Here are some {genre} {era} songs:**\n\n"
    for idx, track in enumerate(tracks, start=1):
        name = track['name']
        artist = track['artists'][0]['name']
        url = track['external_urls']['spotify']
        message += f"{idx}. [{name}]({url}) — {artist}\n"

    await ctx.send(message)

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

#TODO: add chaewon picture command
#TODO: make the message in embed format or inside a code block
#TODO: add emoji reactions to message as buttons
#TODO: improve recommendation algorithm
#TODO: add le sserafim song command
#TODO: add error handling for Spotify API requests
#TODO: word tracker, count # of words used by users