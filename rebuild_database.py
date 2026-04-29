import json
import random
from datetime import datetime
import urllib.parse
import urllib.request
import ssl
import concurrent.futures
import csv
import io
import requests
import re

# 1. Definições
teams = [
    {"country": "França", "flag": "🇫🇷"},
    {"country": "Espanha", "flag": "🇪🇸"},
    {"country": "Argentina", "flag": "🇦🇷"},
    {"country": "Inglaterra", "flag": "🏴"},
    {"country": "Portugal", "flag": "🇵🇹"},
    {"country": "Brasil", "flag": "🇧🇷"},
    {"country": "Holanda", "flag": "🇳🇱"},
    {"country": "Marrocos", "flag": "🇲🇦"},
    {"country": "Bélgica", "flag": "🇧🇪"},
    {"country": "Alemanha", "flag": "🇩🇪"}
]

team_name_map = {
    "França": "France", "Espanha": "Spain", "Argentina": "Argentina",
    "Inglaterra": "England", "Portugal": "Portugal", "Brasil": "Brazil",
    "Holanda": "Netherlands", "Marrocos": "Morocco", "Bélgica": "Belgium",
    "Alemanha": "Germany"
}
reverse_map = {v: k for k, v in team_name_map.items()}

# Jogadores reais com mais convocações de 2018 a 2026
players_raw = {
    "França": [
        ("Hugo Lloris", "Goleiro", "Los Angeles FC", 37),
        ("Benjamin Pavard", "Lateral Direito", "Inter Milan", 28),
        ("Raphaël Varane", "Zagueiro", "Como", 31),
        ("Presnel Kimpembe", "Zagueiro", "PSG", 28),
        ("Lucas Hernández", "Lateral Esquerdo", "PSG", 28),
        ("N'Golo Kanté", "Volante", "Al-Ittihad", 33),
        ("Paul Pogba", "Meio-campista", "Juventus", 31),
        ("Antoine Griezmann", "Meia Atacante", "Atlético Madrid", 33),
        ("Kylian Mbappé", "Atacante", "Real Madrid", 25),
        ("Kingsley Coman", "Ponta Direita", "Bayern Munich", 27),
        ("Olivier Giroud", "Centroavante", "Los Angeles FC", 37)
    ],
    "Espanha": [
        ("Unai Simón", "Goleiro", "Athletic Bilbao", 26),
        ("Jesús Navas", "Lateral Direito", "Sevilla", 38),
        ("Aymeric Laporte", "Zagueiro", "Al Nassr", 30),
        ("Pau Torres", "Zagueiro", "Aston Villa", 27),
        ("Jordi Alba", "Lateral Esquerdo", "Inter Miami", 35),
        ("Rodri", "Volante", "Manchester City", 28),
        ("Sergio Busquets", "Volante", "Inter Miami", 35),
        ("Koke", "Meio-campista", "Atlético Madrid", 32),
        ("Dani Olmo", "Meia Atacante", "RB Leipzig", 26),
        ("Ferran Torres", "Ponta Direita", "Barcelona", 24),
        ("Álvaro Morata", "Centroavante", "AC Milan", 31)
    ],
    "Argentina": [
        ("Emiliano Martínez", "Goleiro", "Aston Villa", 31),
        ("Nahuel Molina", "Lateral Direito", "Atlético Madrid", 26),
        ("Nicolás Otamendi", "Zagueiro", "Benfica", 36),
        ("Germán Pezzella", "Zagueiro", "River Plate", 32),
        ("Nicolás Tagliafico", "Lateral Esquerdo", "Lyon", 31),
        ("Leandro Paredes", "Volante", "AS Roma", 29),
        ("Rodrigo De Paul", "Meio-campista", "Atlético Madrid", 30),
        ("Giovani Lo Celso", "Meio-campista", "Tottenham", 28),
        ("Lionel Messi", "Atacante", "Inter Miami", 37),
        ("Ángel Di María", "Ponta Direita", "Benfica", 36),
        ("Lautaro Martínez", "Centroavante", "Inter Milan", 26)
    ],
    "Inglaterra": [
        ("Jordan Pickford", "Goleiro", "Everton", 30),
        ("Kyle Walker", "Lateral Direito", "Manchester City", 34),
        ("John Stones", "Zagueiro", "Manchester City", 30),
        ("Harry Maguire", "Zagueiro", "Manchester United", 31),
        ("Kieran Trippier", "Lateral Esquerdo", "Newcastle", 33),
        ("Declan Rice", "Volante", "Arsenal", 25),
        ("Jordan Henderson", "Meio-campista", "Ajax", 34),
        ("Mason Mount", "Meio-campista", "Manchester United", 25),
        ("Raheem Sterling", "Ponta Esquerda", "Arsenal", 29),
        ("Bukayo Saka", "Ponta Direita", "Arsenal", 22),
        ("Harry Kane", "Centroavante", "Bayern Munich", 30)
    ],
    "Portugal": [
        ("Rui Patrício", "Goleiro", "AS Roma", 36),
        ("João Cancelo", "Lateral Direito", "Al Hilal", 30),
        ("Pepe", "Zagueiro", "FC Porto", 41),
        ("Rúben Dias", "Zagueiro", "Manchester City", 27),
        ("Raphaël Guerreiro", "Lateral Esquerdo", "Bayern Munich", 30),
        ("William Carvalho", "Volante", "Real Betis", 32),
        ("João Moutinho", "Meio-campista", "Braga", 37),
        ("Bruno Fernandes", "Meia Atacante", "Manchester United", 29),
        ("Bernardo Silva", "Ponta Direita", "Manchester City", 29),
        ("João Félix", "Atacante", "Chelsea", 24),
        ("Cristiano Ronaldo", "Centroavante", "Al Nassr", 39)
    ],
    "Brasil": [
        ("Alisson Becker", "Goleiro", "Liverpool", 31),
        ("Danilo", "Lateral Direito", "Juventus", 32),
        ("Marquinhos", "Zagueiro", "PSG", 30),
        ("Thiago Silva", "Zagueiro", "Fluminense", 39),
        ("Alex Sandro", "Lateral Esquerdo", "Flamengo", 33),
        ("Casemiro", "Volante", "Manchester United", 32),
        ("Fred", "Meio-campista", "Fenerbahçe", 31),
        ("Lucas Paquetá", "Meia Atacante", "West Ham", 26),
        ("Neymar", "Meia Atacante", "Al Hilal", 32),
        ("Richarlison", "Atacante", "Tottenham", 27),
        ("Gabriel Jesus", "Centroavante", "Arsenal", 27)
    ],
    "Holanda": [
        ("Jasper Cillessen", "Goleiro", "Las Palmas", 35),
        ("Denzel Dumfries", "Lateral Direito", "Inter Milan", 28),
        ("Virgil van Dijk", "Zagueiro", "Liverpool", 33),
        ("Matthijs de Ligt", "Zagueiro", "Manchester United", 24),
        ("Daley Blind", "Lateral Esquerdo", "Girona", 34),
        ("Frenkie de Jong", "Volante", "Barcelona", 27),
        ("Georginio Wijnaldum", "Meio-campista", "Al-Ettifaq", 33),
        ("Davy Klaassen", "Meio-campista", "Inter Milan", 31),
        ("Steven Bergwijn", "Ponta Direita", "Al-Ittihad", 26),
        ("Donyell Malen", "Ponta Esquerda", "Borussia Dortmund", 25),
        ("Memphis Depay", "Centroavante", "Corinthians", 30)
    ],
    "Alemanha": [
        ("Manuel Neuer", "Goleiro", "Bayern Munich", 38),
        ("Joshua Kimmich", "Lateral Direito", "Bayern Munich", 29),
        ("Antonio Rüdiger", "Zagueiro", "Real Madrid", 31),
        ("Niklas Süle", "Zagueiro", "Borussia Dortmund", 28),
        ("Robin Gosens", "Lateral Esquerdo", "Union Berlin", 29),
        ("Ilkay Gündogan", "Meio-campista", "Manchester City", 33),
        ("Toni Kroos", "Meio-campista", "Real Madrid", 34),
        ("Leon Goretzka", "Meio-campista", "Bayern Munich", 29),
        ("Serge Gnabry", "Ponta Direita", "Bayern Munich", 28),
        ("Leroy Sané", "Ponta Esquerda", "Bayern Munich", 28),
        ("Thomas Müller", "Meia Atacante", "Bayern Munich", 34)
    ],
    "Bélgica": [
        ("Thibaut Courtois", "Goleiro", "Real Madrid", 32),
        ("Thomas Meunier", "Lateral Direito", "Lille", 32),
        ("Toby Alderweireld", "Zagueiro", "Royal Antwerp", 35),
        ("Jan Vertonghen", "Zagueiro", "Anderlecht", 37),
        ("Timothy Castagne", "Lateral Esquerdo", "Fulham", 28),
        ("Axel Witsel", "Volante", "Atlético Madrid", 35),
        ("Youri Tielemans", "Meio-campista", "Aston Villa", 27),
        ("Kevin De Bruyne", "Meia Atacante", "Manchester City", 33),
        ("Yannick Carrasco", "Ponta Esquerda", "Al-Shabab", 30),
        ("Dries Mertens", "Ponta Direita", "Galatasaray", 37),
        ("Romelu Lukaku", "Centroavante", "Napoli", 31)
    ],
    "Marrocos": [
        ("Yassine Bounou", "Goleiro", "Al Hilal", 33),
        ("Achraf Hakimi", "Lateral Direito", "PSG", 25),
        ("Romain Saïss", "Zagueiro", "Al-Shabab", 34),
        ("Nayef Aguerd", "Zagueiro", "Real Sociedad", 28),
        ("Noussair Mazraoui", "Lateral Esquerdo", "Manchester United", 26),
        ("Sofyan Amrabat", "Volante", "Fenerbahçe", 27),
        ("Azzedine Ounahi", "Meio-campista", "Marseille", 24),
        ("Selim Amallah", "Meio-campista", "Valencia", 27),
        ("Hakim Ziyech", "Ponta Direita", "Galatasaray", 31),
        ("Sofiane Boufal", "Ponta Esquerda", "Al-Rayyan", 30),
        ("Youssef En-Nesyri", "Centroavante", "Fenerbahçe", 27)
    ]
}

from update_attributes import real_attributes

def generate_attrs(name, pos):
    if name in real_attributes:
        return real_attributes[name]
    if pos == "Goleiro": return {"Ritmo": random.randint(40,55), "Finalização": random.randint(20,30), "Passe": random.randint(60,75), "Drible": random.randint(50,65), "Defesa": random.randint(80,92), "Físico": random.randint(70,85)}
    elif pos == "Zagueiro": return {"Ritmo": random.randint(60,75), "Finalização": random.randint(30,50), "Passe": random.randint(60,75), "Drible": random.randint(50,65), "Defesa": random.randint(80,90), "Físico": random.randint(80,92)}
    elif pos in ["Lateral Direito", "Lateral Esquerdo"]: return {"Ritmo": random.randint(80,92), "Finalização": random.randint(50,70), "Passe": random.randint(70,85), "Drible": random.randint(75,85), "Defesa": random.randint(70,82), "Físico": random.randint(70,85)}
    elif pos in ["Volante", "Meio-campista"]: return {"Ritmo": random.randint(65,80), "Finalização": random.randint(60,80), "Passe": random.randint(80,92), "Drible": random.randint(75,85), "Defesa": random.randint(70,85), "Físico": random.randint(75,88)}
    elif pos in ["Meia Atacante", "Ponta Direita", "Ponta Esquerda"]: return {"Ritmo": random.randint(80,95), "Finalização": random.randint(75,88), "Passe": random.randint(80,92), "Drible": random.randint(85,95), "Defesa": random.randint(40,55), "Físico": random.randint(60,75)}
    else: return {"Ritmo": random.randint(75,90), "Finalização": random.randint(85,95), "Passe": random.randint(65,80), "Drible": random.randint(75,88), "Defesa": random.randint(30,45), "Físico": random.randint(75,90)}

WIKI_NAME_MAP = {
    "Rodri": "Rodri (footballer, born 1996)",
    "Koke": "Koke (footballer, born 1992)",
    "Pepe": "Pepe (footballer, born 1983)",
    "Danilo": "Danilo (footballer, born 1991)",
    "Fred": "Fred (footballer, born 1993)"
}

def fetch_wiki_data(name, fallback_club):
    query_name = WIKI_NAME_MAP.get(name, name)
    image_url = "https://ui-avatars.com/api/?name=" + name.replace(" ", "+") + "&size=500&background=0f172a&color=38bdf8"
    club = fallback_club
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages|revisions&rvprop=content&rvslots=main&titles={urllib.parse.quote(query_name)}&format=json&pithumbsize=500"
        req = urllib.request.Request(url, headers={'User-Agent': 'WorldCupDataApp/1.0 (kterra@worldcup.local)'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            page = next(iter(pages.values()))
            
            if 'thumbnail' in page:
                image_url = page['thumbnail']['source']
                
            if 'revisions' in page:
                content = page['revisions'][0]['slots']['main']['*']
                redirect_match = re.match(r'#REDIRECT\s*\[\[(.*?)\]\]', content, re.IGNORECASE)
                if redirect_match:
                    # Se for redirect, vamos tentar pegar apenas o clube do redirect (não queremos estourar recursão com imagens)
                    redirect_club = get_wiki_club(redirect_match.group(1), fallback_club)
                    return image_url, redirect_club
                    
                match = re.search(r'\|\s*currentclub\s*=\s*(.*?)\n', content, re.IGNORECASE)
                if match:
                    raw = match.group(1)
                    raw = re.sub(r'<!--.*?-->', '', raw)
                    raw = re.sub(r'\{\{.*?\}\}', '', raw)
                    link_match = re.search(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', raw)
                    if link_match:
                        club = link_match.group(1).strip()
                    else:
                        club = raw.strip()
                        
                    if not club or club.startswith('|'):
                        club = fallback_club
    except Exception:
        pass
        
    import time
    time.sleep(0.1) # Prevents HTTP 429 Too Many Requests
    
    return image_url, club

def get_wiki_club(name, fallback_club):
    # Função auxiliar para o redirect
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&titles={urllib.parse.quote(name)}&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'WorldCupDataApp/1.0 (kterra@worldcup.local)'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            page = next(iter(pages.values()))
            if 'revisions' in page:
                content = page['revisions'][0]['slots']['main']['*']
                match = re.search(r'\|\s*currentclub\s*=\s*(.*?)\n', content, re.IGNORECASE)
                if match:
                    raw = match.group(1)
                    raw = re.sub(r'<!--.*?-->', '', raw)
                    raw = re.sub(r'\{\{.*?\}\}', '', raw)
                    link_match = re.search(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', raw)
                    if link_match:
                        return link_match.group(1).strip()
                    return raw.strip()
    except Exception:
        pass
    return fallback_club

def get_world_cups(name, age):
    known = {
        "Lionel Messi": ["2006", "2010", "2014", "2018", "2022"],
        "Cristiano Ronaldo": ["2006", "2010", "2014", "2018", "2022"],
        "Antoine Griezmann": ["2014", "2018", "2022"],
        "Kylian Mbappé": ["2018", "2022"],
        "Olivier Giroud": ["2014", "2018", "2022"],
        "Ángel Di María": ["2010", "2014", "2018", "2022"],
        "Nicolás Otamendi": ["2010", "2018", "2022"],
        "Neymar": ["2014", "2018", "2022"],
        "Thiago Silva": ["2014", "2018", "2022"],
        "Marquinhos": ["2018", "2022"],
        "Alisson Becker": ["2018", "2022"],
        "Casemiro": ["2018", "2022"],
        "Danilo": ["2018", "2022"],
        "Harry Kane": ["2018", "2022"],
        "Kyle Walker": ["2018", "2022"],
        "John Stones": ["2018", "2022"],
        "Kevin De Bruyne": ["2014", "2018", "2022"],
        "Romelu Lukaku": ["2014", "2018", "2022"],
        "Jan Vertonghen": ["2014", "2018", "2022"],
        "Marc-André ter Stegen": ["2018", "2022"],
        "Joshua Kimmich": ["2018", "2022"],
        "Antonio Rüdiger": ["2018", "2022"],
        "Álvaro Morata": ["2022"],
        "Dani Carvajal": ["2018", "2022"],
        "Bruno Fernandes": ["2018", "2022"],
        "Bernardo Silva": ["2018", "2022"],
        "Virgil van Dijk": ["2022"],
        "Daley Blind": ["2014", "2022"],
        "Memphis Depay": ["2014", "2022"],
        "Hakim Ziyech": ["2018", "2022"],
        "Achraf Hakimi": ["2018", "2022"],
        "Yassine Bounou": ["2018", "2022"],
        "Romain Saïss": ["2018", "2022"],
        "Hugo Lloris": ["2010", "2014", "2018", "2022"],
        "Raphaël Varane": ["2014", "2018", "2022"],
        "Paul Pogba": ["2014", "2018"],
        "N'Golo Kanté": ["2018"],
        "Toni Kroos": ["2010", "2014", "2018"],
        "Manuel Neuer": ["2010", "2014", "2018", "2022"],
        "Thomas Müller": ["2010", "2014", "2018", "2022"],
        "Sergio Busquets": ["2010", "2014", "2018", "2022"],
        "Jordi Alba": ["2014", "2018", "2022"],
        "Pepe": ["2010", "2014", "2018", "2022"],
        "Rui Patrício": ["2014", "2018", "2022"],
        "Jordan Henderson": ["2014", "2018", "2022"],
        "Raheem Sterling": ["2014", "2018", "2022"],
        "Thibaut Courtois": ["2014", "2018", "2022"],
        "Toby Alderweireld": ["2014", "2018", "2022"],
        "Dries Mertens": ["2014", "2018", "2022"]
    }
    if name in known: return known[name]
    if age >= 31: return ["2018", "2022"]
    elif age >= 24: return ["2022"]
    return []

# Baixar partidas reais de 2018 a 2026
print("Baixando base de dados de partidas internacionais reais...")
url = 'https://raw.githubusercontent.com/martj42/international_results/master/results.csv'
res = requests.get(url)
reader = csv.DictReader(io.StringIO(res.text))
real_matches_by_team = {t: [] for t in team_name_map.keys()}
start_date = datetime(2018, 1, 1) # Desde Janeiro de 2018
end_date = datetime.now()

for row in reader:
    if row['home_score'] == 'NA' or row['away_score'] == 'NA': continue
    match_date = datetime.strptime(row['date'], '%Y-%m-%d')
    if start_date <= match_date <= end_date:
        h_team_en, a_team_en = row['home_team'], row['away_team']
        h_team_pt, a_team_pt = reverse_map.get(h_team_en), reverse_map.get(a_team_en)
        comp = row['tournament']
        if "Friendly" in comp: comp = "Amistoso Internacional"
        elif "qualification" in comp.lower(): comp = "Eliminatórias"
        elif "Nations League" in comp: comp = "Liga das Nações"
        elif "World Cup" in comp: comp = "Copa do Mundo"
        elif "Copa América" in comp or "Euro" in comp or "African Cup" in comp: comp = "Copa Continental"
        
        if h_team_pt: real_matches_by_team[h_team_pt].append({"date": match_date.strftime("%d/%m/%Y"), "competition": comp, "match": f"{h_team_pt} {row['home_score']} x {row['away_score']} {a_team_en}", "team_goals": int(row['home_score']), "dt": match_date})
        if a_team_pt: real_matches_by_team[a_team_pt].append({"date": match_date.strftime("%d/%m/%Y"), "competition": comp, "match": f"{a_team_en} {row['home_score']} x {row['away_score']} {a_team_pt}", "team_goals": int(row['away_score']), "dt": match_date})

for t in real_matches_by_team:
    real_matches_by_team[t] = sorted(real_matches_by_team[t], key=lambda x: x["dt"], reverse=True)

db = []
for country, players in players_raw.items():
    prefix = country[:3].lower()
    for idx, (name, pos, club, age) in enumerate(players):
        p_id = f"{prefix}_{idx+1}"
        attrs = generate_attrs(name, pos)
        goals = int(attrs["Finalização"] * random.uniform(0.1, 0.3)) if pos not in ["Goleiro", "Zagueiro"] else random.randint(0, 3)
        assists = int(attrs["Passe"] * random.uniform(0.1, 0.25)) if pos != "Goleiro" else 0
        
        player_matches = []
        base_matches = real_matches_by_team[country]
        birth_year = 2026 - age
        
        for m in base_matches:
            match_year = m["dt"].year
            age_at_match = match_year - birth_year
            if age_at_match < 18:
                status = "Não Utilizado"
            else:
                # Estes são os jogadores *mais convocados* do período, então a chance de jogar é altíssima
                status = random.choices(["Titular", "Reserva Utilizado", "Não Utilizado"], weights=[0.85, 0.10, 0.05])[0]
                
            minutes = 0; m_goals = 0; m_assists = 0
            if status == "Titular":
                minutes = random.randint(60, 90)
                if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"]:
                    if attrs.get("Finalização", 50) > 80: m_goals = random.randint(0, min(2, m["team_goals"]))
                    else: m_goals = random.randint(0, min(1, m["team_goals"]))
                    m_assists = random.randint(0, min(1, m["team_goals"] - m_goals))
            elif status == "Reserva Utilizado":
                minutes = random.randint(10, 45)
                if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"] and attrs.get("Finalização", 50) > 80:
                    m_goals = random.randint(0, min(1, m["team_goals"]))
                    
            stats_str = f"{minutes} min"
            if m_goals > 0: stats_str += f" | {m_goals} Gols"
            if m_assists > 0: stats_str += f" | {m_assists} Ast"
            player_matches.append({"date": m["date"], "match": m["match"], "competition": m["competition"], "status": status, "stats": stats_str if minutes > 0 else "-"})

        db.append({
            "id": p_id,
            "name": name,
            "country": country,
            "position": pos,
            "age": age,
            "photo_url": "",
            "club": club,
            "world_cups": get_world_cups(name, age),
            "caps_since_2018": sum(1 for m in player_matches if m['status'] != "Não Utilizado"),
            "attributes": attrs,
            "club_performance": {"goals": goals, "assists": assists, "matches": random.randint(25, 45)},
            "recent_callups": player_matches
        })

print("Buscando imagens e clubes atualizados na Wikipedia...")
for p in db:
    image_url, club = fetch_wiki_data(p["name"], p["club"])
    p["photo_url"] = image_url
    if club:
        p["club"] = club

with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"teams": teams, "players": db}, f, ensure_ascii=False, indent=2)

print("Base de dados de 2018 recriada com os jogadores REAIS mais convocados do período!")
