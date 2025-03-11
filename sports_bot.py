import telebot

CHAVE_API = "7521785307:AAGqTZK6NL3CAgDOx6FEhZoq0btPMDodvx0"

bot = telebot.TeleBot(CHAVE_API)

@bot.message_handler(commands=['opcao1'])
def exibir_placares(mensagem):
    pass

@bot.message_handler(commands=['opcao2'])
def exibir_tabelas(mensagem):
    pass

@bot.message_handler(commands=['opcao3'])
def exibir_estatisticas(mensagem):
    pass

@bot.message_handler(commands=['opcao4'])
def proximos_jogos(mensagem):
    pass

def inicio():
    return True

@bot.message_handler(func=inicio)
def mensagem_inicial(mensagem):
    bot.reply_to(mensagem,'''🏆 Bem-vindo ao Bot de Esportes! ⚽

    Aqui você fica por dentro de tudo sobre futebol em tempo real! Escolha uma das opções abaixo para acessar as informações que deseja:
    
    /opcao1 Placar ao Vivo – Confira os resultados das partidas em andamento.
    /opcao2 Tabela de Classificação – Veja a posição dos times nos campeonatos.
    /opcao3 Estatísticas – Acompanhe números detalhados de times e jogadores.
    /opcao4 Próximos Jogos – Descubra quando e onde será a próxima partida do seu time.
    
    Digite o número da opção desejada e comece a explorar o mundo do futebol! ⚽🔥''')


bot.polling()

