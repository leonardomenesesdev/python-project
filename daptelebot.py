from api_football import TELEBOT_TOKEN, FOOTBALL_TOKEN
import telebot, requests

base_url = 'http://api.football-data.org/v4/'

headers = {
    'X-Auth-Token': FOOTBALL_TOKEN
}

bot = telebot.TeleBot(TELEBOT_TOKEN)


def obter_tabela_campeonato(campeonato_id):
    endpoint = f'competitions/{campeonato_id}/standings'
    url = base_url + endpoint

    response = requests.get(url, headers=headers)
       
    dados = response.json()
    return dados

siglas_alteradas = {
    "REC": "SPT",
    "FBP": "GRE",
    "PAU": "SAO"
}
def imprimir_siglas(time):
    sigla = time['team']['tla']
    if sigla in siglas_alteradas:
        sigla = siglas_alteradas[sigla]
    
    sigla_time = " " if time['position'] < 10 else ""
    for letra in sigla:
        sigla_time += letra
    
    espaco = 10 - len(sigla_time) if time['position'] < 10 else 9 - len(sigla_time)
    sigla_time += " " * espaco
    
    return sigla_time

nomes_alterados = {
    "Recife": "Sport",
    "Mineiro": "Atlético Mineiro"
}
def imprimirNomes(time):
    nome = time['team']['shortName']
    if nome in nomes_alterados:
        nome = nomes_alterados[nome]
    
    nome_time = " " if time['position'] < 10 else ""
    for letra in nome:
        nome_time += letra
    
    espaco = 15 - len(nome_time) if time['position'] < 10 else 14 - len(nome_time)
    nome_time += " " * espaco
    
    return nome_time

tabela = obter_tabela_campeonato(2013)

@bot.message_handler(commands=["start"])
def enviarTabela(mensagem):
    chat_id = mensagem.chat.id
    tabela_brasileirao = ""

    try:
        tabela_brasileirao += (f"Tabela do {tabela['competition']['name']}\n")
        tabela_brasileirao += (f"Pos     Time{21 * " "}Pnts   V   E   D   SG\n")
        for time in tabela['standings'][0]['table']:
            sigla_time = imprimir_siglas(time)
            nome_time = imprimirNomes(time)
            tabela_brasileirao += (f"{time['position']}\.  `{nome_time}`    {time['points']}     {time['won']}    {time['draw']}    {time['lost']}    \{time['goalDifference']}\n")

        bot.send_message(chat_id, tabela_brasileirao, parse_mode= 'MarkdownV2')   
    except Exception as e:
        print("Não foi possível obter a tabela.")
        print(e)
  

bot.polling()
