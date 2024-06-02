import discord
import os
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from config.ApiDeamon import fetch_game_data

# Funcție pentru a crea banner-ul
def create_banner(image_url, server_info, image_path=None):
    # Dimensiuni banner
    width, height = 500, 200

    # Descarcă imaginea de fundal
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Verifică dacă URL-ul este accesibil
        background = Image.open(BytesIO(response.content))
        background = background.resize((width, height))
    except Exception as e:
        print(f"Eroare la descărcarea imaginii: {e}")
        return None

    # Desenează peste imagine
    draw = ImageDraw.Draw(background)

    # Încearcă să folosești un font disponibil local
    font_path = "server/banner/font/Roboto-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"Font file not found at {font_path}")
        return None

    try:
        font = ImageFont.truetype(font_path, 20)
    except OSError as e:
        print(f"Failed to load the font: {e}")
        return None

    # Informații de afișat
    game_type = server_info.get('game_type', 'Unknown').capitalize()
    version = server_info.get('version', 'Unknown')
    map_name = server_info.get('map_name', 'Unknown')
    total_players = server_info.get('total_players', 'Unknown')
    country_code = server_info.get('country_code', 'Unknown')

    text = f"Game: {game_type}\nVersion: {version}\nMap: {map_name}\nTotal Players: {total_players}\nCountry: {country_code}"

    # Scrie textul pe imagine
    draw.text((10, 10), text, fill="white", font=font)

    # Adaugă imaginea opțională în dreapta
    if image_path:
        try:
            image = Image.open(image_path)
            image.thumbnail((100, 100))  # Redimensionează imaginea
            background.paste(image, (400, 50))  # Poziționează imaginea în dreapta
        except Exception as e:
            print(f"Eroare la adăugarea imaginii: {e}")

    # Salvează imaginea în fișier temporar
    temp_file = "teml/banner.png"
    try:
        background.save(temp_file)
        return temp_file
    except Exception as e:
        print(f"Eroare la salvarea banner-ului: {e}")
        return None

# Funcție pentru a obține informațiile serverului
async def fetch_game_data(server_ip):
    try:
        # Implementează logica de preluare a datelor despre server folosind adresa IP și portul furnizate
        pass  # Înlocuiește 'pass' cu logica reală pentru a prelua datele despre server
    except Exception as e:
        print(f"Eroare la preluarea datelor de la server: {e}")


# Funcție pentru a obține informațiile serverului
async def get_server_info(server_ip):
    # Definește portul implicit sau utilizează un port specific, dacă este cunoscut
    port = 27015  # Port implicit pentru serverele de jocuri, puteți ajusta la nevoie

    try:
        # Așteaptă rezultatul funcției asincrone pentru a obține datele despre server
        server_data = await fetch_game_data(server_ip)

        # Restul codului rămâne neschimbat
        game_type = find_keyword(server_data, {'game', 'gamename', 'gameset', 'gametype'}).capitalize()
        version = find_keyword(server_data, {'version', 'txadmin-version'})
        map_name = find_keyword(server_data, {'map'})
        total_players = len(server_data.get('players', []))
        country_code = find_keyword(server_data, {'locale', 'country_code'})

        return {
            'game_type': game_type,
            'version': version,
            'map_name': map_name,
            'total_players': total_players,
            'country_code': country_code
        }

    except (KeyError, TypeError) as e:
        print("Eroare în procesarea datelor de la server:")
        print(e)
        return None


# Funcție pentru a găsi valoarea unui cuvânt cheie într-un dicționar
def find_keyword(data, keywords):
    for key, value in data.items():
        if key.lower() in keywords:
            return value
        if isinstance(value, dict):
            found = find_keyword(value, keywords)
            if found:
                return found
    return 'Unknown'