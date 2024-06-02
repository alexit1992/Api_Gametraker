import discord
import os
import requests
from PIL import Image
from io import BytesIO

######################################### FORMAT TIME #########################################

def format_time(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

#########################################  FORMAT SERVER INFO ######################################### 

def format_server_info(server_ip, server_info):
    server_data = server_info.get(server_ip, {})
    embed = discord.Embed(title="", color=discord.Color.green())

    if not server_data:
        embed.add_field(name="Eroare", value="Serverul specificat nu a putut fi găsit.", inline=False)
        return embed

    #########################################  { Funcție pentru a găsi valoarea unui cuvânt cheie într-un dicționar } ######################################### 
    
    def find_keyword(data, keywords):
        for key, value in data.items():
            if key.lower() in keywords:
                return value
            if isinstance(value, dict):
                found = find_keyword(value, keywords)
                if found:
                    return found
        return 'Ping'

    #########################################  Cuvinte cheie pentru joc ######################################### 

    game_keywords = {'game', 'gamename', 'gameset', 'gametype'}
    game_type = find_keyword(server_data.get('raw', {}), game_keywords).lower()

    # Adaugă iconiță lângă câmpul `Game` (folosind un emoji)
    game_field_name = f"🕹️ Game"
    embed.add_field(name=game_field_name, value=game_type.capitalize(), inline=True)

    ##########################################  Cuvinte cheie pentru versiune ######################################### 

    version_keywords = {'version', 'txadmin-version'}
    version = find_keyword(server_data.get('raw', {}), version_keywords)
    
    # Adaugă iconiță lângă câmpul `Version`
    version_field_name = f"📝 Version"
    embed.add_field(name=version_field_name, value=version, inline=True)


    #########################################   Adaugă numele hărții în locul adecvat ######################################### 

    map_name = server_data.get('map', 'Map unavailable')
    
    # Adaugă iconiță lângă câmpul `Map`
    map_field_name = f"🗺️ Map"
    embed.add_field(name=map_field_name, value=map_name, inline=True)

    #########################################  Adaugă numărul total de jucători online în locul adecvat #########################################  

    total_players = len(server_data.get('players', []))
    
    # Adaugă iconiță lângă câmpul `Total Online Players`
    total_players_field_name = f"👥 Total Online Players"
    embed.add_field(name=total_players_field_name, value=total_players, inline=True)


    #########################################  Cuvânt cheie pentru țară ######################################### 

    country_keywords = {'locale', 'country'}

    # Detectarea țării serverului pe baza country
    country_flags = {
        'US': 'https://www.countryflags.io/us/flat/64.png',
        'RO': 'https://www.countryflags.io/ro/flat/64.png',
        'DE': 'https://www.countryflags.io/de/flat/64.png',
        # Adaugă aici mai multe țări după cum este necesar
    }

    country = find_keyword(server_data.get('raw', {}), country_keywords)
    country_code = country.upper() if country else 'Unavailable'
    country_flag_url = country_flags.get(country_code, '')

    #########################################  Adaugă câmpul pentru țară ######################################### 

    # Adaugă iconiță lângă câmpul `Country`
    country_field_name = f"🌍 Country"
    embed.add_field(name=country_field_name, value=country_code, inline=True)

    #########################################  Adaugă steagul țării dacă este disponibil ######################################### 

    # Obțineți URL-ul imaginii de banner
    #info_icon_url = server_data.get('raw', {}).get('info', {}).get('vars', {}).get('banner_connecting', '')

    # Verificați dacă există un URL pentru imagine
    #if info_icon_url:
        # Setează thumbnail-ul cu URL-ul imaginii de banner
        #embed.set_thumbnail(url=info_icon_url)
    #else:
        #print("Eroare: Nu s-a găsit URL pentru imagine.")

    table_content = "```\n"
    table_content += f"{'👤':<2}|{'Name':<10}{'Score':<10} {'TimePlayed':<20} {'Ping':<10}\n"
    table_content += "-" * 56 + "\n"

    players_info = server_data.get('players', [])
    players_info.sort(key=lambda x: x.get('raw', {}).get('score', 0), reverse=True)

    for player_data in players_info[:15]:
        name = player_data.get('name', 'Unknown')
        icon = "👤"
        if len(name) < 4:
            name = f"{name}"  # Adaugă trei puncte în fața numelui
        elif len(name) > 4:
            name = name[:4] + '🫂'  # Taie numele la 5 caractere și adaugă iconița la final
        else:
            name += '🫂'  # Adaugă iconița la finalul numelui
        score = player_data.get('raw', {}).get('score', 'N/A')
        time_spent = player_data.get('raw', {}).get('time', 0)
        formatted_time = format_time(time_spent)

       #########################################  Caută și afișează informațiile despre ping ######################################### 

        ping_keywords = {'ping'}
        ping = find_keyword(player_data.get('raw', {}), ping_keywords)

        table_content += f"{icon: <2}|{name: <10}|{score: <10}{formatted_time: <20}{ping: <10}\n"

    table_content += "```"

    # Obțineți numele serverului din răspunsul API-ului
    nume_server = server_data.get('name', 'Nume nedisponibil')

    # Limitați numele serverului la maxim 13 caractere
    if len(nume_server) > 40:
        nume_server = nume_server[:40]

    # Construiți valoarea pentru câmpul 'Online Players' care va include și numele serverului
    players_field_value = f"{nume_server}\n{table_content}"

    # Adăugați câmpul 'Online Players' în cadrul embed-ului, cu numele serverului pe aceeași linie
    embed.add_field(name="Online Players", value=players_field_value, inline=False)

    if server_data.get('status', '') == 'online':
        embed.color = discord.Color.green()
    else:
        embed.color = discord.Color.red()

    return embed

# Funcție pentru a obține dimensiunile imaginii de la URL
def get_image_dimensions(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img.size
    except Exception as e:
        print(f"Eroare la obținerea dimensiunilor imaginii: {e}")
        return None

# Funcție pentru a seta dimensiunile imaginii și a o afișa într-un chenar specific
def set_image_with_dimensions(embed, url, max_size):
    try:
        # Obține dimensiunile imaginii de la URL
        dimensions = get_image_dimensions(url)
        if dimensions:
            # Calculează dimensiunile adecvate pentru a încadra imaginea într-un chenar pătrat
            width, height = dimensions
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            # Setează thumbnail-ul cu URL-ul imaginii de banner și dimensiunile calculate
            embed.set_thumbnail(url=url)
            embed.set_thumbnail(width=new_width, height=new_height)
        else:
            print("Eroare: Dimensiunile imaginii nu au putut fi obținute.")
    except Exception as e:
        print(f"Eroare la setarea imaginii: {e}")
