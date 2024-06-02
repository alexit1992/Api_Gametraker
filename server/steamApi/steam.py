import os
import requests
import discord
from discord.ext import commands
from config.config import STEAM_API_KEY

# Define emoji icons
ICON_REAL_NAME = ":bust_in_silhouette:"
ICON_LOCATION = ":round_pushpin:"
ICON_STATUS = ":computer:"
ICON_BADGES = ":medal:"
ICON_FAVORITE_GAME = ":video_game:"
ICON_MOST_PLAYED_GAME = ":joystick:"

def format_status(status):
    status_dict = {
        0: "Offline",
        1: "Online",
        2: "Busy",
        3: "Away",
        4: "Snooze",
        5: "Looking to trade",
        6: "Looking to play"
    }
    return status_dict.get(status, 'Unavailable')

def format_badges(badges):
    formatted_badges = []
    for badge in badges[:5]:  # Limităm la primele 5 badge-uri
        badge_str = f"Badge ID: {badge['badgeid']} | Level: {badge['level']} | XP: {badge['xp']}"
        formatted_badges.append(badge_str)
    return "\n".join(formatted_badges)

async def create_embed(username, profile_url, avatar_url, real_name, location, status, badges, favorite_game, most_played_game):
    # Verificăm lungimea câmpurilor și ajustăm-le dacă este necesar
    real_name = real_name[:50]  # Limităm lungimea numelui reale la 50 de caractere
    location = location[:50]    # Limităm lungimea locației la 50 de caractere
    status = status[:50]        # Limităm lungimea statusului la 50 de caractere

    # Formatează lista de badge-uri
    badges_str = format_badges(badges)
    favorite_game_str = str(favorite_game)
    most_played_game_str = str(most_played_game)

    # Reducem lungimea valorilor la maxim 1024 de caractere
    badges_str = badges_str[:1024]
    favorite_game_str = favorite_game_str[:1024]
    most_played_game_str = most_played_game_str[:1024]

    # Cream încorporarea Discord cu informațiile furnizate
    embed = discord.Embed(title=f"{username}'s Steam Profile", url=profile_url, color=discord.Color.blue())
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name=f"{ICON_REAL_NAME} Real Name", value=real_name, inline=True)
    embed.add_field(name=f"{ICON_LOCATION} Location", value=location, inline=True)
    embed.add_field(name=f"{ICON_STATUS} Status", value=status, inline=True)
    embed.add_field(name=f"{ICON_BADGES} Badges", value=badges_str, inline=False)
    embed.add_field(name=f"{ICON_FAVORITE_GAME} Favorite Game", value=favorite_game_str, inline=False)
    embed.add_field(name=f"{ICON_MOST_PLAYED_GAME} Most Played Game", value=most_played_game_str, inline=False)

    return embed

async def search_steam_user(identifier):
    try:
        if identifier.isdigit() and len(identifier) == 17:
            url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={identifier}"
        else:
            url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={identifier}"
            response = requests.get(url)
            data = response.json()
            if 'response' in data and 'steamid' in data['response']:
                steam_id = data['response']['steamid']
                url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"

        response = requests.get(url)
        data = response.json()
        if 'response' in data and 'players' in data['response'] and data['response']['players']:
            return data['response']['players'][0]
        return None
    except Exception as e:
        print("Error searching Steam user:", e)
        return None

async def get_badges(steam_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetBadges/v1/?key={STEAM_API_KEY}&steamid={steam_id}"
        response = requests.get(url)
        data = response.json()

        if 'response' in data and 'badges' in data['response']:
            badges = data['response']['badges']
            if badges:
                return badges
        return []
    except Exception as e:
        print("Error fetching badges:", e)
        return []


async def get_favorite_game(steam_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json"
        response = requests.get(url)
        data = response.json()
        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            if games:
                # Sortăm jocurile după timpul jucat pentru a obține jocul preferat
                favorite_game = sorted(games, key=lambda x: x.get('playtime_forever', 0), reverse=True)[0]
                return favorite_game.get('name', 'Unknown Game')
        return "No Favorite Game Found"
    except Exception as e:
        print("Error fetching favorite game:", e)
        return "Error Fetching Favorite Game"


async def get_most_played_game(steam_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}"
        response = requests.get(url)
        data = response.json()

        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            if games:
                # Sortăm lista de jocuri după numărul de ore jucate
                sorted_games = sorted(games, key=lambda x: x['playtime_forever'], reverse=True)
                # Returnăm cel mai jucat joc (primul joc din lista sortată)
                most_played_game = sorted_games[0]['name']
                return most_played_game
        return "No Most Played Game Found"
    except Exception as e:
        print("Error fetching most played game:", e)
        return "Error Fetching Most Played Game"