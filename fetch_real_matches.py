import json
import csv
import io
import requests
from datetime import datetime
import random

# Mapa de nomes do JSON para nomes no CSV em inglês
team_name_map = {
    "França": "France",
    "Espanha": "Spain",
    "Argentina": "Argentina",
    "Inglaterra": "England",
    "Portugal": "Portugal",
    "Brasil": "Brazil",
    "Holanda": "Netherlands",
    "Marrocos": "Morocco",
    "Bélgica": "Belgium",
    "Alemanha": "Germany"
}

reverse_map = {v: k for k, v in team_name_map.items()}

# 1. Carregar dados locais
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Baixar resultados reais
print("Baixando base de dados de partidas internacionais reais...")
url = 'https://raw.githubusercontent.com/martj42/international_results/master/results.csv'
res = requests.get(url)
reader = csv.DictReader(io.StringIO(res.text))

# 3. Filtrar partidas reais
real_matches_by_team = {t: [] for t in team_name_map.keys()}

# Considerando data limite entre Setembro de 2018 e Abril de 2026 (presente no env)
start_date = datetime(2018, 8, 1)
end_date = datetime.now() # O env diz que hoje é Abril 2026

for row in reader:
    if row['home_score'] == 'NA' or row['away_score'] == 'NA':
        continue
    
    match_date = datetime.strptime(row['date'], '%Y-%m-%d')
    if start_date <= match_date <= end_date:
        h_team_en = row['home_team']
        a_team_en = row['away_team']
        
        # Verificar se algum dos times é do nosso Top 10
        h_team_pt = reverse_map.get(h_team_en)
        a_team_pt = reverse_map.get(a_team_en)
        
        # Formatar competição
        comp = row['tournament']
        if "Friendly" in comp: comp = "Amistoso Internacional"
        elif "qualification" in comp.lower(): comp = "Eliminatórias"
        elif "Nations League" in comp: comp = "Liga das Nações"
        elif "World Cup" in comp: comp = "Copa do Mundo"
        elif "Copa América" in comp or "Euro" in comp or "African Cup" in comp: comp = "Copa Continental"
        
        if h_team_pt:
            real_matches_by_team[h_team_pt].append({
                "date": match_date.strftime("%d/%m/%Y"),
                "competition": comp,
                "match": f"{h_team_pt} {row['home_score']} x {row['away_score']} {a_team_en}",
                "team_goals": int(row['home_score']),
                "dt": match_date
            })
            
        if a_team_pt:
            real_matches_by_team[a_team_pt].append({
                "date": match_date.strftime("%d/%m/%Y"),
                "competition": comp,
                "match": f"{a_team_en} {row['home_score']} x {row['away_score']} {a_team_pt}",
                "team_goals": int(row['away_score']),
                "dt": match_date
            })

# Ordenar matches do mais recente para o mais antigo
for t in real_matches_by_team:
    real_matches_by_team[t] = sorted(real_matches_by_team[t], key=lambda x: x["dt"], reverse=True)

# 4. Atualizar jogadores com as partidas reais
for p in data['players']:
    country = p['country']
    base_matches = real_matches_by_team[country]
    player_matches = []
    pos = p.get('position', 'Meio-campista')
    
    birth_year = 2026 - p['age']
    
    for m in base_matches:
        match_year = m["dt"].year
        age_at_match = match_year - birth_year
        
        if age_at_match < 18:
            status = "Não Utilizado"
        else:
            # Veteranos e estrelas têm alta probabilidade
            status = random.choices(["Titular", "Reserva Utilizado", "Não Utilizado"], weights=[0.65, 0.20, 0.15])[0]
            
        minutes = 0; goals = 0; assists = 0
        
        if status == "Titular":
            minutes = random.randint(60, 90)
            if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"]:
                if p["attributes"].get("Finalização", 50) > 80:
                    goals = random.randint(0, min(2, m["team_goals"]))
                else:
                    goals = random.randint(0, min(1, m["team_goals"]))
                assists = random.randint(0, min(1, m["team_goals"] - goals))
        elif status == "Reserva Utilizado":
            minutes = random.randint(10, 45)
            if m["team_goals"] > 0 and pos not in ["Goleiro", "Zagueiro"]:
                if p["attributes"].get("Finalização", 50) > 80:
                    goals = random.randint(0, min(1, m["team_goals"]))
        
        stats_str = f"{minutes} min"
        if goals > 0: stats_str += f" | {goals} Gols"
        if assists > 0: stats_str += f" | {assists} Ast"
            
        # Remover a chave dt que não é serializável ou não precisamos no JSON final
        clean_match = {
            "date": m["date"],
            "match": m["match"],
            "competition": m["competition"],
            "status": status,
            "stats": stats_str if minutes > 0 else "-"
        }
        player_matches.append(clean_match)
        
    p['recent_callups'] = player_matches
    p['caps_since_2018'] = sum(1 for m in player_matches if m['status'] != "Não Utilizado")
    
    if 'caps_since_2022' in p:
        del p['caps_since_2022']

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Partidas reais de 2018 em diante integradas com sucesso!")
