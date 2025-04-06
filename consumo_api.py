import requests

api_token = "62e2a71b1a174f3988c64667be34589a"

times = [
    {'nome': 'Palmeiras', 'ID': 176},
    {'nome': 'Corinthians', 'ID': 759},
    {'nome': 'São Paulo', 'ID': 762},
    {'nome': 'Santos', 'ID': 763},
    {'nome': 'Flamengo', 'ID': 1377}
]

print('Times disponíveis:\n')
for time in times:
    print(f"- {time['nome']}")
print('')

encontrado = False
while not encontrado:
    time_escolhido = input('Digite o time que deseja consultar: ').strip().lower()

    for time in times:
        if time['nome'].lower() == time_escolhido:
            encontrado = True
            team_id = time['ID']
            nome_time = time['nome']
            break

    if not encontrado:
        print('Time não encontrado. Tente novamente.')

url = f"http://api.football-data.org/v4/teams/{team_id}/matches"

headers = {
    "X-Auth-Token": api_token
}

params = {
    'status': 'SCHEDULED',
    'limit': 5
}

try:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        matches = data.get("matches", [])

        print(f"\nPróximas partidas do {nome_time}:\n")
        for match in matches:
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            date = match["utcDate"][:10]
            competition = match["competition"]["name"]

            print(f"{date} - {home} vs {away} ({competition})")
    else:
        print("Erro ao buscar dados:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("Erro de conexão com a API:", e)
