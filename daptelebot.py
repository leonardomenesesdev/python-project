from api_football import obter_tabela_campeonato, imprimirNomes, imprimirSiglas, TELEBOT_TOKEN
import telebot

bot = telebot.TeleBot(TELEBOT_TOKEN)

tabela = obter_tabela_campeonato(2013)

@bot.message_handler(commands=["start"])
def enviarTabela(mensagem):
    chat_id = mensagem.chat.id
    tabelaBrasileirao = ""

    try:
        # tabelaBrasileirao += (f"Tabela do {tabela['competition']['name']}\n")
        # tabelaBrasileirao += ("Pos     Time         Pnts   V   D   E   SG\n")
        # for time in tabela['standings'][0]['table']:
        #     tabelaBrasileirao += (f"{time['position']}.  {imprimirNomes(time)}   {time['points']}     {time['won']}   {time['lost']}   {time['draw']}   {time['goalDifference']}\n")
        tabelaBrasileirao += (f"Tabela do {tabela['competition']['name']}\n")
        tabelaBrasileirao += ("Pos     Time        Pnts   V   E   D   SG\n")
        for time in tabela['standings'][0]['table']:
            sigla_time = imprimirSiglas(time)
            nome_time = imprimirNomes(time)
            tabelaBrasileirao += (f"{time['position']}\.  `{sigla_time}`   {time['points']}     {time['won']}    {time['draw']}    {time['lost']}    \{time['goalDifference']}\n")
        
    except:
        print("Não foi possível obter a tabela.")

    teste = "1\. `time` 3pts 0V 1D 3E \-2SG"

    bot.send_message(chat_id, tabelaBrasileirao, parse_mode= 'MarkdownV2')   

bot.polling()