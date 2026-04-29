import json
import random
from datetime import datetime, timedelta

competitions = ["Amistoso Internacional", "Eliminatórias", "Liga das Nações", "Copa Continental"]
opponents = ["Itália", "Croácia", "Uruguai", "Senegal", "México", "EUA", "Japão", "Suíça", "Dinamarca", "Colômbia", "Sérvia", "Polônia", "Chile", "Suécia", "Nigéria"]

def generate_matches(country):
    matches = []
    # Começando logo após a copa de 2022 (Ex: Março de 2023)
    start_date = datetime(2023, 3, 20)
    # Gerando cerca de 15 partidas até 2026
    for i in range(15):
        date = start_date + timedelta(days=i*24 + random.randint(-5, 10))
        opp = random.choice(opponents)
        comp = random.choice(competitions)
        is_home = random.choice([True, False])
        
        # Gerar placar realista
        goals_home = random.randint(0, 4)
        goals_away = random.randint(0, 2) if is_home else random.randint(0, 3)
        
        if is_home:
            score = f"{country} {goals_home} x {goals_away} {opp}"
            team_goals = goals_home
        else:
            score = f"{opp} {goals_home} x {goals_away} {country}"
            team_goals = goals_away
            
        matches.append({
            "date": date.strftime("%d/%m/%Y"),
            "competition": comp,
            "match": score,
            "team_goals": team_goals
        })
    # Ordenar da mais recente para a mais antiga
    return sorted(matches, key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True)

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

country_matches = {}
for team in data['teams']:
    country_matches[team['country']] = generate_matches(team['country'])

for p in data['players']:
    country = p['country']
    base_matches = country_matches[country]
    player_matches = []
    
    for m in base_matches:
        # Probabilidade do jogador jogar
        status = random.choices(["Titular", "Reserva Utilizado", "Não Utilizado"], weights=[0.75, 0.15, 0.10])[0]
        minutes = 0
        goals = 0
        assists = 0
        
        if status == "Titular":
            minutes = random.randint(60, 90)
            if m["team_goals"] > 0:
                # Se é atacante/meia, tem mais chance de gol
                if p["attributes"]["Shooting"] > 80:
                    goals = random.randint(0, min(2, m["team_goals"]))
                else:
                    goals = random.randint(0, min(1, m["team_goals"]))
                assists = random.randint(0, min(1, m["team_goals"] - goals))
                
        elif status == "Reserva Utilizado":
            minutes = random.randint(10, 45)
            if m["team_goals"] > 0:
                if p["attributes"]["Shooting"] > 80:
                    goals = random.randint(0, min(1, m["team_goals"]))
        
        stats_str = f"{minutes} min"
        if goals > 0:
            stats_str += f" | {goals} Gols"
        if assists > 0:
            stats_str += f" | {assists} Ast"
            
        player_matches.append({
            "date": m["date"],
            "match": m["match"],
            "competition": m["competition"],
            "status": status,
            "stats": stats_str if minutes > 0 else "-"
        })
        
    p['recent_callups'] = player_matches
    p['caps_since_2022'] = sum(1 for m in player_matches if m['status'] != "Não Utilizado")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Histórico de convocações atualizado com sucesso!")
