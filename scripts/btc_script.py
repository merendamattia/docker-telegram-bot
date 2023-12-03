import requests
import threading
import time
import asyncio

from telethon import events

# Comando per ottenere le fee di BTC
def btc_fees():
    data = get_data("https://mempool.space/api/v1/fees/recommended")
    reply = "Priority (sat/vB): \n"
    reply += "High: " + get_fees("FASTEST", data) + "\n"
    reply += "Med: " + get_fees("HALFHOUR", data) + "\n"
    reply += "Slow: " + get_fees("HOUR", data) + "\n"
    reply += "Very slow: " + get_fees("ECONOMY", data) + "\n"
    reply += "Minimum: " + get_fees("MINIMUM", data) + "\n"

    return reply

async def tracking_function_btcfees(value, event):
    # Crea un thread che eseguirà la funzione di ascolto
    asyncio.create_task(tracking_thread_btcfees(value, event))
    await event.respond("Thread started")

async def tracking_thread_btcfees(value, event):
    c = 0
    event_occurred = False
    await event.respond("tracking_thread_btcfees in")
    await event.respond(event_occurred)

    while not event_occurred:
        await event.respond("GET Request n=" + str(c))
        c += 1

        # Esegui la tua azione di tracking, ad esempio, effettua una richiesta GET
        data = get_data("https://mempool.space/api/v1/fees/recommended")
        minimum = get_fees("MINIMUM", data)

        await event.respond("GET Request done")
        await event.respond(data)
        await event.respond(minimum)
        
        # Verifica l'evento o la risposta
        if value >= minimum:
            await event.respond("TARGET RAGGIUNTO!!! " + str(value))
            # Imposta la variabile di controllo per far terminare il thread
            event_occurred = True

        seconds = 10
        await event.respond("sleep " + str(seconds) + " seconds")
        # Attendi 30 secondi prima di eseguire nuovamente la richiesta
        await asyncio.sleep(seconds)
    
    await event.respond("Thread dead")
# ---------------------------------------- FUNZIONI VARIE
# Effettua una richiesta GET a un URL e ottiene i dati JSON
def get_data(url):
    response = requests.get(url)
    data = response.json()
    return data

# Serve per il comando BTCfees, ritorna le fees
def get_fees(type, data):
    inizio = 0
    fine = 0
    switch_dict = {
        "FASTEST": "fastestFee",
        "HALFHOUR": "halfHourFee",
        "HOUR": "hourFee",
        "ECONOMY": "economyFee",
        "MINIMUM": "minimumFee"
    }

    if type != "MINIMUM":
        inizio = data[switch_dict[type]] + 3
        fine = data[switch_dict[type]]
    else:
        inizio = data[switch_dict[type]] + 3
        fine = data[switch_dict[type]]

    return str(fine)

