import requests

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

