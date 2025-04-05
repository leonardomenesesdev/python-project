import requests
API_KEY = "79267e85a8a14f7ba6f6b924361a8fda"
BASE_URL ="https://api.football-data.org/v4"
HEADERS = {
    'X-Auth-Token': API_KEY
}

def getRodada(rodada):
    url = f"{BASE_URL}/competitions/BSA/matches?matchday={rodada}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json
    else:
        print(f"Erro em getRodada")
        return None
    
