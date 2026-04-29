import json
import random
from datetime import datetime, timedelta
import urllib.parse
import urllib.request
import ssl
import concurrent.futures

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

players_raw = {
    "França": [
        ("Mike Maignan", "Goleiro", "AC Milan", 28),
        ("Jules Koundé", "Lateral Direito", "Barcelona", 25),
        ("Dayot Upamecano", "Zagueiro", "Bayern Munich", 25),
        ("William Saliba", "Zagueiro", "Arsenal", 23),
        ("Theo Hernández", "Lateral Esquerdo", "AC Milan", 26),
        ("Aurélien Tchouaméni", "Volante", "Real Madrid", 24),
        ("Adrien Rabiot", "Meio-campista", "Juventus", 29),
        ("Antoine Griezmann", "Meia Atacante", "Atlético Madrid", 33),
        ("Ousmane Dembélé", "Ponta Direita", "PSG", 27),
        ("Kylian Mbappé", "Atacante", "Real Madrid", 25),
        ("Olivier Giroud", "Centroavante", "Los Angeles FC", 37)
    ],
    "Espanha": [
        ("Unai Simón", "Goleiro", "Athletic Bilbao", 26),
        ("Dani Carvajal", "Lateral Direito", "Real Madrid", 32),
        ("Robin Le Normand", "Zagueiro", "Atlético Madrid", 27),
        ("Aymeric Laporte", "Zagueiro", "Al Nassr", 30),
        ("Marc Cucurella", "Lateral Esquerdo", "Chelsea", 25),
        ("Rodri", "Volante", "Manchester City", 28),
        ("Fabián Ruiz", "Meio-campista", "PSG", 28),
        ("Pedri", "Meio-campista", "Barcelona", 21),
        ("Lamine Yamal", "Ponta Direita", "Barcelona", 16),
        ("Nico Williams", "Ponta Esquerda", "Athletic Bilbao", 21),
        ("Álvaro Morata", "Centroavante", "AC Milan", 31)
    ],
    "Argentina": [
        ("Emiliano Martínez", "Goleiro", "Aston Villa", 31),
        ("Nahuel Molina", "Lateral Direito", "Atlético Madrid", 26),
        ("Cristian Romero", "Zagueiro", "Tottenham", 26),
        ("Nicolás Otamendi", "Zagueiro", "Benfica", 36),
        ("Nicolás Tagliafico", "Lateral Esquerdo", "Lyon", 31),
        ("Rodrigo De Paul", "Meio-campista", "Atlético Madrid", 30),
        ("Enzo Fernández", "Meio-campista", "Chelsea", 23),
        ("Alexis Mac Allister", "Meio-campista", "Liverpool", 25),
        ("Lionel Messi", "Atacante", "Inter Miami", 37),
        ("Ángel Di María", "Ponta Direita", "Benfica", 36),
        ("Julián Álvarez", "Centroavante", "Atlético Madrid", 24)
    ],
    "Inglaterra": [
        ("Jordan Pickford", "Goleiro", "Everton", 30),
        ("Kyle Walker", "Lateral Direito", "Manchester City", 34),
        ("John Stones", "Zagueiro", "Manchester City", 30),
        ("Harry Maguire", "Zagueiro", "Manchester United", 31),
        ("Luke Shaw", "Lateral Esquerdo", "Manchester United", 28),
        ("Declan Rice", "Volante", "Arsenal", 25),
        ("Jude Bellingham", "Meia Atacante", "Real Madrid", 21),
        ("Phil Foden", "Meia Atacante", "Manchester City", 24),
        ("Bukayo Saka", "Ponta Direita", "Arsenal", 22),
        ("Marcus Rashford", "Ponta Esquerda", "Manchester United", 26),
        ("Harry Kane", "Centroavante", "Bayern Munich", 30)
    ],
    "Portugal": [
        ("Diogo Costa", "Goleiro", "FC Porto", 24),
        ("João Cancelo", "Lateral Direito", "Al Hilal", 30),
        ("Rúben Dias", "Zagueiro", "Manchester City", 27),
        ("Gonçalo Inácio", "Zagueiro", "Sporting CP", 22),
        ("Nuno Mendes", "Lateral Esquerdo", "PSG", 22),
        ("João Palhinha", "Volante", "Bayern Munich", 28),
        ("Vitinha", "Meio-campista", "PSG", 24),
        ("Bruno Fernandes", "Meia Atacante", "Manchester United", 29),
        ("Bernardo Silva", "Meia Atacante", "Manchester City", 29),
        ("Rafael Leão", "Ponta Esquerda", "AC Milan", 25),
        ("Cristiano Ronaldo", "Centroavante", "Al Nassr", 39)
    ],
    "Brasil": [
        ("Alisson Becker", "Goleiro", "Liverpool", 31),
        ("Danilo", "Lateral Direito", "Juventus", 32),
        ("Marquinhos", "Zagueiro", "PSG", 30),
        ("Gabriel Magalhães", "Zagueiro", "Arsenal", 26),
        ("Guilherme Arana", "Lateral Esquerdo", "Atlético Mineiro", 27),
        ("Casemiro", "Volante", "Manchester United", 32),
        ("Bruno Guimarães", "Meio-campista", "Newcastle", 26),
        ("Lucas Paquetá", "Meia Atacante", "West Ham", 26),
        ("Raphinha", "Ponta Direita", "Barcelona", 27),
        ("Vinícius Júnior", "Ponta Esquerda", "Real Madrid", 23),
        ("Rodrygo", "Atacante", "Real Madrid", 23)
    ],
    "Holanda": [
        ("Bart Verbruggen", "Goleiro", "Brighton", 21),
        ("Denzel Dumfries", "Lateral Direito", "Inter Milan", 28),
        ("Virgil van Dijk", "Zagueiro", "Liverpool", 33),
        ("Nathan Aké", "Zagueiro", "Manchester City", 29),
        ("Daley Blind", "Lateral Esquerdo", "Girona", 34),
        ("Jerdy Schouten", "Volante", "PSV", 27),
        ("Tijjani Reijnders", "Meio-campista", "AC Milan", 25),
        ("Frenkie de Jong", "Meio-campista", "Barcelona", 27),
        ("Xavi Simons", "Meia Atacante", "RB Leipzig", 21),
        ("Cody Gakpo", "Ponta Esquerda", "Liverpool", 25),
        ("Memphis Depay", "Atacante", "Corinthians", 30)
    ],
    "Marrocos": [
        ("Yassine Bounou", "Goleiro", "Al Hilal", 33),
        ("Achraf Hakimi", "Lateral Direito", "PSG", 25),
        ("Nayef Aguerd", "Zagueiro", "West Ham", 28),
        ("Romain Saïss", "Zagueiro", "Al-Shabab", 34),
        ("Noussair Mazraoui", "Lateral Esquerdo", "Manchester United", 26),
        ("Sofyan Amrabat", "Volante", "Fenerbahçe", 27),
        ("Azzedine Ounahi", "Meio-campista", "Marseille", 24),
        ("Selim Amallah", "Meio-campista", "Valencia", 27),
        ("Hakim Ziyech", "Ponta Direita", "Galatasaray", 31),
        ("Sofiane Boufal", "Ponta Esquerda", "Al-Rayyan", 30),
        ("Youssef En-Nesyri", "Centroavante", "Fenerbahçe", 27)
    ],
    "Bélgica": [
        ("Koen Casteels", "Goleiro", "Al Qadsiah", 32),
        ("Timothy Castagne", "Lateral Direito", "Fulham", 28),
        ("Wout Faes", "Zagueiro", "Leicester City", 26),
        ("Jan Vertonghen", "Zagueiro", "Anderlecht", 37),
        ("Arthur Theate", "Lateral Esquerdo", "Eintracht Frankfurt", 24),
        ("Amadou Onana", "Volante", "Aston Villa", 22),
        ("Youri Tielemans", "Meio-campista", "Aston Villa", 27),
        ("Kevin De Bruyne", "Meia Atacante", "Manchester City", 33),
        ("Jérémy Doku", "Ponta Esquerda", "Manchester City", 22),
        ("Leandro Trossard", "Ponta Esquerda", "Arsenal", 29),
        ("Romelu Lukaku", "Centroavante", "Napoli", 31)
    ],
    "Alemanha": [
        ("Marc-André ter Stegen", "Goleiro", "Barcelona", 32),
        ("Joshua Kimmich", "Lateral Direito", "Bayern Munich", 29),
        ("Antonio Rüdiger", "Zagueiro", "Real Madrid", 31),
        ("Jonathan Tah", "Zagueiro", "Bayer Leverkusen", 28),
        ("Maximilian Mittelstädt", "Lateral Esquerdo", "VfB Stuttgart", 27),
        ("Robert Andrich", "Volante", "Bayer Leverkusen", 29),
        ("Pascal Groß", "Meio-campista", "Borussia Dortmund", 33),
        ("Florian Wirtz", "Meia Atacante", "Bayer Leverkusen", 21),
        ("Jamal Musiala", "Meia Atacante", "Bayern Munich", 21),
        ("Leroy Sané", "Ponta Direita", "Bayern Munich", 28),
        ("Kai Havertz", "Atacante", "Arsenal", 25)
    ]
}

def generate_attrs(pos):
    if pos == "Goleiro":
        return {"Ritmo": random.randint(40,55), "Finalização": random.randint(20,30), "Passe": random.randint(60,75), "Drible": random.randint(50,65), "Defesa": random.randint(80,92), "Físico": random.randint(70,85)}
    elif pos == "Zagueiro":
        return {"Ritmo": random.randint(60,75), "Finalização": random.randint(30,50), "Passe": random.randint(60,75), "Drible": random.randint(50,65), "Defesa": random.randint(80,90), "Físico": random.randint(80,92)}
    elif pos in ["Lateral Direito", "Lateral Esquerdo"]:
        return {"Ritmo": random.randint(80,92), "Finalização": random.randint(50,70), "Passe": random.randint(70,85), "Drible": random.randint(75,85), "Defesa": random.randint(70,82), "Físico": random.randint(70,85)}
    elif pos in ["Volante", "Meio-campista"]:
        return {"Ritmo": random.randint(65,80), "Finalização": random.randint(60,80), "Passe": random.randint(80,92), "Drible": random.randint(75,85), "Defesa": random.randint(70,85), "Físico": random.randint(75,88)}
    elif pos in ["Meia Atacante", "Ponta Direita", "Ponta Esquerda"]:
        return {"Ritmo": random.randint(80,95), "Finalização": random.randint(75,88), "Passe": random.randint(80,92), "Drible": random.randint(85,95), "Defesa": random.randint(40,55), "Físico": random.randint(60,75)}
    else: # Atacante / Centroavante
        return {"Ritmo": random.randint(75,90), "Finalização": random.randint(85,95), "Passe": random.randint(65,80), "Drible": random.randint(75,88), "Defesa": random.randint(30,45), "Físico": random.randint(75,90)}

def get_wiki_image(name):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(name)}&prop=pageimages&format=json&pithumbsize=500"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode())
            pages = res.get('query', {}).get('pages', {})
            for page_id in pages:
                if 'thumbnail' in pages[page_id]:
                    return pages[page_id]['thumbnail']['source']
    except Exception:
        pass
    return "https://ui-avatars.com/api/?name=" + name.replace(" ", "+") + "&size=500&background=0f172a&color=38bdf8"

# Matches generation
competitions = ["Amistoso Internacional", "Eliminatórias", "Liga das Nações", "Copa Continental"]
opponents = ["Itália", "Croácia", "Uruguai", "Senegal", "México", "EUA", "Japão", "Suíça", "Dinamarca", "Colômbia", "Sérvia", "Polônia", "Chile", "Suécia", "Nigéria"]

def generate_matches(country):
    matches = []
    start_date = datetime(2023, 3, 20)
    for i in range(15):
        date = start_date + timedelta(days=i*24 + random.randint(-5, 10))
        opp = random.choice(opponents)
        comp = random.choice(competitions)
        is_home = random.choice([True, False])
        goals_home = random.randint(0, 4)
        goals_away = random.randint(0, 2) if is_home else random.randint(0, 3)
        if is_home:
            score = f"{country} {goals_home} x {goals_away} {opp}"
            team_goals = goals_home
        else:
            score = f"{opp} {goals_home} x {goals_away} {country}"
            team_goals = goals_away
        matches.append({"date": date.strftime("%d/%m/%Y"), "competition": comp, "match": score, "team_goals": team_goals})
    return sorted(matches, key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True)

country_matches = {team['country']: generate_matches(team['country']) for team in teams}

db = []
for country, players in players_raw.items():
    prefix = country[:3].lower()
    for idx, (name, pos, club, age) in enumerate(players):
        p_id = f"{prefix}_{idx+1}"
        attrs = generate_attrs(pos)
        
        # Player performance
        goals = int(attrs["Finalização"] * random.uniform(0.1, 0.3)) if pos not in ["Goleiro", "Zagueiro"] else random.randint(0, 3)
        assists = int(attrs["Passe"] * random.uniform(0.1, 0.25)) if pos != "Goleiro" else 0
        
        # Generate match history
        player_matches = []
        for m in country_matches[country]:
            status = random.choices(["Titular", "Reserva Utilizado", "Não Utilizado"], weights=[0.75, 0.15, 0.10])[0]
            minutes = 0; m_goals = 0; m_assists = 0
            if status == "Titular":
                minutes = random.randint(60, 90)
                if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"]:
                    m_goals = random.randint(0, min(1 if pos in ["Volante", "Lateral Direito", "Lateral Esquerdo"] else 2, m["team_goals"]))
                    m_assists = random.randint(0, min(1, m["team_goals"] - m_goals))
            elif status == "Reserva Utilizado":
                minutes = random.randint(10, 45)
                if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"]:
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
            "photo_url": "", # Will be populated
            "club": club,
            "caps_since_2022": sum(1 for m in player_matches if m['status'] != "Não Utilizado"),
            "attributes": attrs,
            "club_performance": {"goals": goals, "assists": assists, "matches": random.randint(25, 45)},
            "recent_callups": player_matches
        })

print("Fetching Wikipedia images...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(get_wiki_image, p["name"]): p for p in db}
    for future in concurrent.futures.as_completed(futures):
        p = futures[future]
        p["photo_url"] = future.result()

with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"teams": teams, "players": db}, f, ensure_ascii=False, indent=2)

print("11 players per team generated successfully!")
