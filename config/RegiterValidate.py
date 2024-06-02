#########################################  Importarea librăriilor necesare #########################################

import logging
import bcrypt

#########################################  Importarea From librăriilor necesare #########################################

from datetime import datetime
from config.config import get_db_connection, mysql


######################################### Funcția de validare și criptare a datelor #########################################

async def validate_and_encrypt(email: str, dateofbirth: str, password: str):
    try:

        ######################################### Criptarea parolei ######################################### 
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        #########################################  Verifică formatul datei de naștere ######################################### 

        dateofbirth_obj = datetime.strptime(dateofbirth, "%d-%m-%Y").date()

        return hashed_password, dateofbirth_obj

    except Exception as e:
        logging.error(f'Eroare la validarea și criptarea datelor: {e}')
        return None, None

async def register_user(ctx, email: str, dateofbirth: str, password: str):
    player_id = ctx.author.id
    user_name = ctx.author.name

    #########################################  Validarea și criptarea datelor ######################################### 

    hashed_password, dateofbirth_obj = await validate_and_encrypt(email, dateofbirth, password)

    if hashed_password is None or dateofbirth_obj is None:
        await ctx.send('Eroare la înregistrare. Te rog să verifici datele introduse.')
        return

    try:
        #########################################  Obține conexiunea la baza de date ######################################### 

        db = get_db_connection()
        cursor = db.cursor()

        #########################################  Verifică dacă utilizatorul este deja înregistrat ######################################### 

        cursor.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
        result = cursor.fetchone()

        if result:
            await ctx.send(f'{user_name}, ești deja înregistrat.')
        else:
            #########################################  Înregistrează utilizatorul în baza de date ######################################### 

            cursor.execute(
                "INSERT INTO players (player_id, username, email, dateofbirth, password) VALUES (%s, %s, %s, %s, %s)",
                (player_id, user_name, email, dateofbirth_obj, hashed_password)
            )
            db.commit()
            await ctx.send(f'{user_name}, ai fost înregistrat cu succes!')

        #########################################  Închide cursorul și conexiunea ######################################### 

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        print(f'Eroare la înregistrarea utilizatorului: {err}')
        await ctx.send('A apărut o problemă la conectarea la baza de date. Încearcă din nou mai târziu.')
