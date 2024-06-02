######################################### {1} {Do not delete these Imports} {Nu le ștergeți Importurile} #################################################
import os
import discord
import logging
import bcrypt
import requests

######################################### {2} {This is the import of files} {Acesta este importul fișierelor} ####################################
from dotenv import load_dotenv
from config.config import get_db_connection, STEAM_API_KEY
from datetime import datetime
from discord.ext import commands
from config.ApiDeamon import fetch_game_data
from server.FormatServerInfo import format_server_info
from config.RegiterValidate import register_user
from grade.grades import add_role, find_member_by_name, available_roles
from config.vulgare import citeste_cuvinte_vulgare, cenzureaza_mesaj
from reload import reload_modules_in_directory
from server.steamApi.steam import search_steam_user, create_embed, get_badges, get_favorite_game, get_most_played_game, format_status
from server.banner.CreateBanner import create_banner, get_server_info

########################################## {3} {Încarcă variabilele din fișierul .env} {Load variables from the .env file} ##########################
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Conectați-vă la baza de date folosind config.py
db = get_db_connection()
cursor = db.cursor()

######################################### {4} {Creează directorul logs dacă nu există} {Configurează logging-ul} ###################


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

logger = logging.getLogger(__name__)


# Calea către fișierul cu cuvintele vulgare
cale_fisier_cuvinte_vulgare = 'server/cuvinte_vulgare.txt'


######################################### {5} {Create an instance of the Discord Bot} {Crează o instanță a Botului Discord} ###################

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='/', intents=intents)

# Calea către fonturile Roboto și Noto Color Emoji
ROBOTO_FONT_PATH = "/server/banner/font/Roboto-Regular.ttf"  # Schimbă cu calea reală către fontul Roboto descărcat
EMOJI_FONT_PATH = "/server/banner/font/NotoColorEmoji.ttf"  # Schimbă cu calea reală către fontul Noto Color Emoji descărcat
BACKGROUND_IMAGE_PATH = "./server/baner3.gif"  # Schimbă cu calea reală către imaginea de fundal

# Dimensiunile dorite pentru imaginea de fundal
BACKGROUND_WIDTH = 400  # Schimbă cu lățimea dorită
BACKGROUND_HEIGHT = 100  # Schimbă cu înălțimea dorită

######################################### {6} {Defining bot events} {Definirea evenimentelor botului} ###############################################

@bot.event
async def on_ready():
    logger.info(f'Conectat ca {bot.user}')
    print(f'Conectat ca {bot.user}')

######################################### ACEASTA ESTE COMANDA JOIN CHEANEL ###########################################

@bot.command()
async def join(ctx):
    if ctx.author.voice:  
        channel = ctx.author.voice.channel  
        voice_client = ctx.voice_client  

        ######################################### Verificăm dacă botul este deja conectat la un canal vocal #########################################

        if voice_client and voice_client.channel:
            if voice_client.channel == channel:
                await ctx.send("Botul este deja pe acest canal vocal!")
                return
            else:
                await voice_client.move_to(channel) 
        else:
            await channel.connect() 
        await ctx.send(f"Botul a fost invitat pe canalul vocal {channel.name}!")
    else:
        await ctx.send("Nu ești conectat la niciun canal vocal!")

######################################### {7} {Here are the commands used} {Aici sunt comenzile folosite} ###########################################

@bot.command()
async def server(ctx, server_ip):
    try:
        server_info = await fetch_game_data(server_ip)
        if server_info:
            embed = format_server_info(server_ip, server_info)
            await ctx.send(embed=embed)
            logger.info(f'Informații server trimise pentru {server_ip}')
        else:
            await ctx.send("Eroare la obținerea informațiilor despre server.")
            logger.error(f'Eroare la obținerea informațiilor despre server pentru {server_ip}')
    except Exception as e:
        await ctx.send("A apărut o eroare.")
        logger.exception(f'Eroare la procesarea comenzii server pentru {server_ip}: {e}')

@bot.command()
async def serverbanner(ctx, server_ip: str, image_url: str, optional_image_url: str = None):
    try:
        # Obține informațiile serverului folosind doar adresa IP
        server_info_data = await get_server_info(server_ip)

        if server_info_data is None:
            await ctx.send("Nu s-au putut obține datele de la server.")
            return

        # Restul codului rămâne neschimbat
        banner_path = create_banner(image_url, server_info_data)

        if banner_path:
            await ctx.send(file=discord.File(banner_path))
        else:
            await ctx.send("A apărut o eroare la generarea banner-ului.")
    except ValueError as e:
        print("Eroare în despartirea adresei IP și a portului:", e)
        await ctx.send("Adresa IP trebuie să fie în formatul 'ip:port'.")

    
        
######################################### Steamprofile Commands ###########################################
 
@bot.command()
async def steamprofile(ctx, identifier):
    try:
        player_info = await search_steam_user(identifier)
        if player_info:
            steam_id = player_info.get('steamid')
            badges = await get_badges(steam_id)
            favorite_game = await get_favorite_game(steam_id)
            most_played_game = await get_most_played_game(steam_id)
            embed = await create_embed(
                player_info.get('personaname'),
                player_info.get('profileurl'),
                player_info.get('avatarfull'),
                player_info.get('realname', 'N/A'),
                player_info.get('loccountrycode', 'N/A'),
                format_status(player_info.get('personastate')),
                badges,
                favorite_game,
                most_played_game
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Unable to find Steam profile for this user.")
    except Exception as e:
        await ctx.send("An error occurred while searching for Steam profile.")
        print(f"Error: {e}")



async def validate_and_encrypt(email: str, dateofbirth: str, password: str):
    try:
        ######################################### {Criptarea parolei} ###########################################

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        ######################################### {Verifică formatul datei de naștere} ###########################################

        dateofbirth_obj = datetime.strptime(dateofbirth, "%Y-%m-%d").date()

        return hashed_password, dateofbirth_obj

    except Exception as e:
        print(f'Eroare la validarea și criptarea datelor: {e}')
        return None, None
    

######################################### { Register } ###########################################

@bot.command()
async def register(ctx, email: str, dateofbirth: str, password: str):
    await register_user(ctx, email, dateofbirth, password)


######################################### { ADD_ROLE} ###########################################
@bot.command()
async def role(ctx, member_name, role_name):
    guild = ctx.guild
    if guild is None:
        await ctx.send("Această comandă poate fi folosită doar pe un server.")
        return

    member = await find_member_by_name(guild, member_name)
    if member is None:
        await ctx.send(f"Membrul '{member_name}' nu a putut fi găsit pe acest server.")
        return

    ######################################### { Verificăm dacă rolul există pe server } ###########################################

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Rolul '{role_name}' nu există pe acest server.")
        return

    ########################################### { Adăugăm rolul membrului } ###########################################
    try:
        await member.add_roles(role)
        await ctx.send(f"Rolul '{role_name}' a fost atribuit membrului '{member.name}'.")
    except discord.Forbidden:
        await ctx.send("Nu am permisiunea să atribui acest rol.")
    except Exception as e:
        await ctx.send(f"A apărut o eroare în timpul atribuirii rolului: {e}")


########################################### { CHECK ROLES } ###########################################
@bot.command()
async def checkr(ctx, member: discord.Member):
    roles = [role.name for role in member.roles]
    await ctx.send(f"Gradele membrului {member.mention} sunt: {', '.join(roles[1:])}")



################### {8} {Definirea răspunsurilor la mesaje} ###################

@bot.event
async def on_message(message):
    # Verifică dacă mesajul a fost trimis de un alt bot sau este privat
    if message.author.bot or isinstance(message.channel, discord.DMChannel):
        return

    # Lista de cuvinte vulgare
    cuvinte_vulgare = citeste_cuvinte_vulgare()

    # Verifică dacă mesajul conține un cuvânt vulgar
    for cuvant in cuvinte_vulgare:
        if cuvant in message.content.lower():
            # Cenzurează mesajul
            mesaj_cenzurat = cenzureaza_mesaj(message.content, cuvinte_vulgare)
            # Șterge mesajul cu cuvântul vulgar
            await message.delete()
            # Creează un mesaj embed cu avertismentul și o imagine atașată
            embed = discord.Embed(title="AVERTISMENT", description=f"Mesaj cu cuvânt vulgar detectat de la {message.author.mention}:", color=discord.Color.red())
            embed.add_field(name="Mesaj cenzurat:", value=mesaj_cenzurat, inline=False)
            embed.set_image(url="https://media.tenor.com/e4FbvQFnpMUAAAAC/no-never.gif")
            # Trimite mesajul embed în canalul specific
            await message.channel.send(embed=embed)
            break

    # Verifică dacă mesajul este comanda /server ip:port

    await bot.process_commands(message)  # Asigură-te că și alte comenzi sunt procesate normal



################### {9} {Rulează botul} ###################
try:
    bot.run(TOKEN)
except Exception as e:
    logger.exception(f'Eroare la rularea botului: {e}')
