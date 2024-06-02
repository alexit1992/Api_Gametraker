######################################### {1} {Do not delete these Imports} {Nu le ștergeți Importurile} #################################################
import os
import mysql.connector
from dotenv import load_dotenv

########################################## {3} {Încarcă variabilele din fișierul .env} {Load variables from the .env file} ##########################
load_dotenv()

########################################## {Preia variabilele de mediu MYSQL API_KEY YOUTUBE} ##########################################
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
API_TOKEN = os.getenv('API_TOKEN')
API_TOKEN_TYPE = os.getenv('API_TOKEN_TYPE')
API_TOKEN_EMAIL = os.getenv('API_TOKEN_EMAIL')
API_KEY = os.getenv('API_KEY')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')


def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
