import requests

url = "https://api.football-data.org/v4/competitions/BSA/matches?matchday=2"
headers = {
    "X-Auth-Token": "79267e85a8a14f7ba6f6b924361a8fda"  # Substitua pela sua chave real
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    for partida in dados["matches"][:5]:  # Mostra só as 5 primeiras
        home = partida['homeTeam']['name']
        away = partida['awayTeam']['name']
        status = partida['status']
        print(f"{home} x {away} | Status: {status}")
else:
    print("Erro:", response.status_code)
    print(response.json())
