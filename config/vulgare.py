import discord
import os


# Calea către fișierul cu cuvintele vulgare
cale_fisier_cuvinte_vulgare = 'server/cuvinte_vulgare.txt'

# Funcție pentru a citi cuvintele vulgare din fișier
def citeste_cuvinte_vulgare():
    cuvinte_vulgare = []
    try:
        with open(cale_fisier_cuvinte_vulgare, 'r') as file:
            for line in file:
                cuvant = line.strip()  # Elimină spațiile albe și newline-ul de la sfârșitul fiecărui rând
                cuvinte_vulgare.append(cuvant)
    except FileNotFoundError:
        print(f'Fișierul "{cale_fisier_cuvinte_vulgare}" nu a fost găsit.')
    return cuvinte_vulgare

# Funcție pentru a înlocui cuvintele vulgare cu "*"
def cenzureaza_mesaj(mesaj, cuvinte_vulgare):
    for cuvant in cuvinte_vulgare:
        mesaj = mesaj.replace(cuvant, '*' * len(cuvant))
    return mesaj