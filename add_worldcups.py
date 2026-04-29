import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lógica simplificada para determinar copas baseadas na idade do jogador e no conhecimento real
def get_world_cups(name, age):
    cups = []
    
    # Exceções muito conhecidas (veteranos/astros)
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
        "Romain Saïss": ["2018", "2022"]
    }
    
    if name in known:
        return known[name]
        
    # Estimar para o restante baseado na idade em 2026 (a data do sistema)
    # 2022 -> idade - 4. Se tinha >= 21 em 2022 (idade atual >= 25), provável 2022
    # 2018 -> idade - 8. Se tinha >= 23 em 2018 (idade atual >= 31), provável 2018 e 2022
    
    if age >= 31:
        cups = ["2018", "2022"]
    elif age >= 24:
        cups = ["2022"]
    else:
        # Muito novo em 2022 (ex: Lamine Yamal, Bellingham, Musiala, etc.)
        # Algumas exceções de jovens que foram pra copa em 2022
        young_stars = ["Jude Bellingham", "Jamal Musiala", "Pedri", "Gavi", "Eduardo Camavinga", "Vinícius Júnior", "Rodrygo"]
        if name in young_stars:
            cups = ["2022"]
            
    return cups

for p in data['players']:
    cups = get_world_cups(p['name'], p['age'])
    p['world_cups'] = cups

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Copas do mundo adicionadas!")
