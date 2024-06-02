import discord
import os
from discord.ext import commands
from config.ApiDeamon import fetch_game_data
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import asyncio

# Lista cu cadrul de imagini pentru animație
image_frames = []

# Funcție pentru a încărca cadrele de imagine
def load_image_frames():
    global image_frames
    for i in range(1, 11):  # Încarcă 10 cadre de imagine numerotate de la 1 la 10
        image_path = f"frame_{i}.png"  # Ajustează calea către fișierul de imagine
        if os.path.exists(image_path):
            image_frames.append(Image.open(image_path))
        else:
            print(f"Imaginea {image_path} nu a putut fi găsită.")

# Funcție pentru a crea banner-ul animat
async def create_animated_banner(ctx):
    load_image_frames()  # Încarcă cadrele de imagine
    if not image_frames:
        await ctx.send("Eroare la încărcarea imaginilor.")
        return

    # Intervalul de timp în secunde între cadre (ajustează după preferințe)
    frame_interval = 0.1

    # Schimbă rapid cadrele pentru a crea efectul de animație
    for frame in image_frames:
        # Afișează banner-ul pe canalul Discord
        with BytesIO() as image_binary:
            frame.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, filename='banner.gif'))

        # Așteaptă un interval între cadre
        await asyncio.sleep(frame_interval)