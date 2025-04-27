from api_football import TELEBOT_TOKEN, FOOTBALL_TOKEN
import telebot, requests,time

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
    
    espaco = 17 - len(nome_time) if time['position'] < 10 else 16 - len(nome_time)
    nome_time += " " * espaco
    
    return nome_time

tabela = obter_tabela_campeonato(2013)

@bot.message_handler(commands=["start"])
def enviarTabela(mensagem):
    chat_id = mensagem.chat.id
    tabela_brasileirao = ""

    try:
        tabela_brasileirao += (f"Tabela do {tabela['competition']['name']}\n")
        tabela_brasileirao += (f"Pos     Time{25 * " "}Pnts   V   E   D   SG\n")
        for time in tabela['standings'][0]['table']:
            sigla_time = imprimir_siglas(time)
            nome_time = imprimirNomes(time)
            tabela_brasileirao += (f"{time['position']}\.  `{nome_time}`    {time['points']}     {time['won']}    {time['draw']}    {time['lost']}    \{time['goalDifference']}\n")

        bot.send_message(chat_id, tabela_brasileirao, parse_mode= 'MarkdownV2')   
    except Exception as e:
        print("Não foi possível obter a tabela.")
        print(e)



def obter_partidas(campeonato_id):
    endpoint = f'competitions/{campeonato_id}/matches'
    url = base_url + endpoint

    response = requests.get(url, headers=headers)
       
    dados = response.json()
    return dados


time_casa = []
time_fora = []
resultado = []
vencedor = []
macth_day = []
dados = obter_partidas(2013)
partidas = dados['matches']
rodadas_geral = []
rodada_atual = [] 
def partidas_finalizadas():
    status = []
    status_atual = "FINISHED"
    i = 0

    while status_atual == "FINISHED":
        status_atual = partidas[i]['status']
        time_casa.append(partidas[i]['homeTeam']['shortName'])
        time_fora.append(partidas[i]['awayTeam']['shortName'])
        resultado.append(f"{partidas[i]['score']['fullTime']['home']} x {partidas[i]['score']['fullTime']['away']}")
        if (partidas[i]['score']['winner']) == "HOME_TEAM":
            vencedor.append((partidas[i]['homeTeam']['shortName']))
        elif (partidas[i]['score']['winner']) == "AWAY_TEAM":
            vencedor.append((partidas[i]['awayTeam']['shortName']))
        elif (partidas[i]['score']['winner']) == "DRAW":
            vencedor.append("Empate")
        macth_day.append(partidas[i]['matchday'])

        
        status.append(status_atual)
        i += 1

    contador_partidas1 = 1
    try:
        while contador_partidas1 < len(time_casa):

            contador_partidas2 = 1
            rodada_atual.clear()

            while contador_partidas2 <= 10:
                partida = {
                    'Time da Casa': "",
                    'Time de Fora': "",
                    'Resultado': "",
                    'Vencedor': "",
                    'Match Day': 0
                    }  
                partida['Time da Casa'] = time_casa[contador_partidas1-1]
                partida['Time de Fora'] = time_fora[contador_partidas1-1]
                partida['Resultado'] = resultado[contador_partidas1-1]
                partida['Vencedor'] = vencedor[contador_partidas1-1]
                partida['Match Day'] = macth_day[contador_partidas1-1]
                
                contador_partidas1 += 1
                contador_partidas2 += 1
                rodada_atual.append(partida)
                
            rodadas_geral.append(rodada_atual)

    except IndexError:
        print("Rodadas acabadas")
   

@bot.message_handler(commands=["rodada"])
def enviarRodada(mensagem):
    partidas_finalizadas()
    chat_id = mensagem.chat.id
    texto_rodada = ""
    for i in rodada_atual:
        texto_rodada += f"{i['Time da Casa']} {i['Resultado']} {i['Time de Fora']}\n" 
    
    bot.send_message(chat_id, texto_rodada)


bot.polling()
