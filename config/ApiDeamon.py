######################################### {Do not delete these Import } {Nu le ștergeți Import} #################################################
import os
import discord
import aiohttp

######################################### { Function to get the server information }  {Funcție pentru a obține informațiile despre server} ###########################
async def fetch_game_data(server_ip):
    try:
        API_TOKEN = os.getenv('API_TOKEN')
        API_TOKEN_TYPE = os.getenv('API_TOKEN_TYPE')
        API_TOKEN_EMAIL = os.getenv('API_TOKEN_EMAIL')

        url = 'https://gamequery.dev/post/fetch'

        headers = {
            'Content-Type': 'application/json',
            'x-api-token': API_TOKEN,
            'x-api-token-type': API_TOKEN_TYPE,
            'x-api-token-email': API_TOKEN_EMAIL,
            'User-Agent': 'Mozilla/5.0 (compatible; GApiPlugin/1.0; +https://gamequery.dev)',
        }

        data = {
            "servers": [server_ip]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()  # Ridică o excepție dacă răspunsul nu este de tip 2xx
                return await response.json()

    except aiohttp.ClientError as e:
        print("Eroare în realizarea cererii:")
        print(e)
        return None