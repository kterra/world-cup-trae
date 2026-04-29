import json

real_attributes = {
    # França
    "Hugo Lloris": {"Ritmo": 50, "Finalização": 25, "Passe": 65, "Drible": 60, "Defesa": 85, "Físico": 65},
    "Benjamin Pavard": {"Ritmo": 74, "Finalização": 58, "Passe": 76, "Drible": 73, "Defesa": 83, "Físico": 79},
    "Raphaël Varane": {"Ritmo": 79, "Finalização": 45, "Passe": 64, "Drible": 65, "Defesa": 85, "Físico": 79},
    "Presnel Kimpembe": {"Ritmo": 76, "Finalização": 35, "Passe": 68, "Drible": 68, "Defesa": 82, "Físico": 85},
    "Lucas Hernández": {"Ritmo": 78, "Finalização": 55, "Passe": 74, "Drible": 74, "Defesa": 83, "Físico": 80},
    "N'Golo Kanté": {"Ritmo": 76, "Finalização": 66, "Passe": 75, "Drible": 81, "Defesa": 85, "Físico": 80},
    "Paul Pogba": {"Ritmo": 70, "Finalização": 79, "Passe": 85, "Drible": 84, "Defesa": 65, "Físico": 83},
    "Antoine Griezmann": {"Ritmo": 79, "Finalização": 86, "Passe": 87, "Drible": 88, "Defesa": 54, "Físico": 70},
    "Kylian Mbappé": {"Ritmo": 97, "Finalização": 90, "Passe": 80, "Drible": 92, "Defesa": 36, "Físico": 78},
    "Kingsley Coman": {"Ritmo": 89, "Finalização": 76, "Passe": 79, "Drible": 87, "Defesa": 30, "Físico": 60},
    "Olivier Giroud": {"Ritmo": 39, "Finalização": 83, "Passe": 71, "Drible": 70, "Defesa": 42, "Físico": 80},
    
    # Espanha
    "Unai Simón": {"Ritmo": 45, "Finalização": 20, "Passe": 70, "Drible": 65, "Defesa": 84, "Físico": 68},
    "Jesús Navas": {"Ritmo": 80, "Finalização": 64, "Passe": 80, "Drible": 81, "Defesa": 75, "Físico": 58},
    "Aymeric Laporte": {"Ritmo": 65, "Finalização": 50, "Passe": 74, "Drible": 69, "Defesa": 86, "Físico": 79},
    "Pau Torres": {"Ritmo": 73, "Finalização": 35, "Passe": 76, "Drible": 72, "Defesa": 84, "Físico": 78},
    "Jordi Alba": {"Ritmo": 82, "Finalização": 69, "Passe": 81, "Drible": 82, "Defesa": 76, "Físico": 70},
    "Rodri": {"Ritmo": 58, "Finalização": 73, "Passe": 86, "Drible": 79, "Defesa": 85, "Físico": 84},
    "Sergio Busquets": {"Ritmo": 42, "Finalização": 62, "Passe": 82, "Drible": 79, "Defesa": 82, "Físico": 73},
    "Koke": {"Ritmo": 68, "Finalização": 73, "Passe": 86, "Drible": 81, "Defesa": 76, "Físico": 78},
    "Dani Olmo": {"Ritmo": 78, "Finalização": 76, "Passe": 83, "Drible": 85, "Defesa": 55, "Físico": 65},
    "Ferran Torres": {"Ritmo": 82, "Finalização": 79, "Passe": 78, "Drible": 83, "Defesa": 35, "Físico": 68},
    "Álvaro Morata": {"Ritmo": 82, "Finalização": 81, "Passe": 70, "Drible": 78, "Defesa": 40, "Físico": 76},

    # Argentina
    "Emiliano Martínez": {"Ritmo": 52, "Finalização": 25, "Passe": 65, "Drible": 60, "Defesa": 86, "Físico": 75},
    "Nahuel Molina": {"Ritmo": 83, "Finalização": 62, "Passe": 76, "Drible": 78, "Defesa": 76, "Físico": 70},
    "Nicolás Otamendi": {"Ritmo": 55, "Finalização": 50, "Passe": 65, "Drible": 58, "Defesa": 83, "Físico": 83},
    "Germán Pezzella": {"Ritmo": 54, "Finalização": 35, "Passe": 55, "Drible": 50, "Defesa": 81, "Físico": 80},
    "Nicolás Tagliafico": {"Ritmo": 78, "Finalização": 55, "Passe": 72, "Drible": 75, "Defesa": 80, "Físico": 78},
    "Leandro Paredes": {"Ritmo": 60, "Finalização": 74, "Passe": 82, "Drible": 80, "Defesa": 75, "Físico": 74},
    "Rodrigo De Paul": {"Ritmo": 78, "Finalização": 76, "Passe": 83, "Drible": 83, "Defesa": 74, "Físico": 82},
    "Giovani Lo Celso": {"Ritmo": 74, "Finalização": 74, "Passe": 83, "Drible": 84, "Defesa": 65, "Físico": 66},
    "Lionel Messi": {"Ritmo": 80, "Finalização": 87, "Passe": 90, "Drible": 94, "Defesa": 33, "Físico": 64},
    "Ángel Di María": {"Ritmo": 79, "Finalização": 79, "Passe": 84, "Drible": 86, "Defesa": 48, "Físico": 58},
    "Lautaro Martínez": {"Ritmo": 83, "Finalização": 86, "Passe": 74, "Drible": 85, "Defesa": 48, "Físico": 84},

    # Inglaterra
    "Jordan Pickford": {"Ritmo": 55, "Finalização": 20, "Passe": 75, "Drible": 65, "Defesa": 83, "Físico": 70},
    "Kyle Walker": {"Ritmo": 90, "Finalização": 63, "Passe": 77, "Drible": 78, "Defesa": 81, "Físico": 82},
    "John Stones": {"Ritmo": 72, "Finalização": 40, "Passe": 76, "Drible": 75, "Defesa": 85, "Físico": 79},
    "Harry Maguire": {"Ritmo": 46, "Finalização": 52, "Passe": 68, "Drible": 65, "Defesa": 81, "Físico": 85},
    "Kieran Trippier": {"Ritmo": 75, "Finalização": 65, "Passe": 84, "Drible": 78, "Defesa": 80, "Físico": 71},
    "Declan Rice": {"Ritmo": 73, "Finalização": 65, "Passe": 80, "Drible": 77, "Defesa": 84, "Físico": 83},
    "Jordan Henderson": {"Ritmo": 65, "Finalização": 70, "Passe": 80, "Drible": 75, "Defesa": 76, "Físico": 76},
    "Mason Mount": {"Ritmo": 74, "Finalização": 76, "Passe": 82, "Drible": 81, "Defesa": 55, "Físico": 64},
    "Raheem Sterling": {"Ritmo": 88, "Finalização": 78, "Passe": 78, "Drible": 86, "Defesa": 45, "Físico": 60},
    "Bukayo Saka": {"Ritmo": 85, "Finalização": 82, "Passe": 81, "Drible": 87, "Defesa": 65, "Físico": 65},
    "Harry Kane": {"Ritmo": 69, "Finalização": 93, "Passe": 84, "Drible": 83, "Defesa": 49, "Físico": 83},

    # Portugal
    "Rui Patrício": {"Ritmo": 45, "Finalização": 25, "Passe": 65, "Drible": 60, "Defesa": 81, "Físico": 70},
    "João Cancelo": {"Ritmo": 84, "Finalização": 73, "Passe": 85, "Drible": 85, "Defesa": 80, "Físico": 71},
    "Pepe": {"Ritmo": 65, "Finalização": 45, "Passe": 60, "Drible": 58, "Defesa": 84, "Físico": 86},
    "Rúben Dias": {"Ritmo": 62, "Finalização": 39, "Passe": 68, "Drible": 68, "Defesa": 89, "Físico": 87},
    "Raphaël Guerreiro": {"Ritmo": 76, "Finalização": 75, "Passe": 86, "Drible": 86, "Defesa": 76, "Físico": 60},
    "William Carvalho": {"Ritmo": 45, "Finalização": 62, "Passe": 77, "Drible": 75, "Defesa": 79, "Físico": 84},
    "João Moutinho": {"Ritmo": 52, "Finalização": 68, "Passe": 84, "Drible": 80, "Defesa": 65, "Físico": 60},
    "Bruno Fernandes": {"Ritmo": 71, "Finalização": 85, "Passe": 90, "Drible": 83, "Defesa": 69, "Físico": 77},
    "Bernardo Silva": {"Ritmo": 69, "Finalização": 78, "Passe": 86, "Drible": 92, "Defesa": 65, "Físico": 68},
    "João Félix": {"Ritmo": 81, "Finalização": 78, "Passe": 79, "Drible": 86, "Defesa": 40, "Físico": 66},
    "Cristiano Ronaldo": {"Ritmo": 77, "Finalização": 88, "Passe": 75, "Drible": 79, "Defesa": 34, "Físico": 74},

    # Brasil
    "Alisson Becker": {"Ritmo": 55, "Finalização": 25, "Passe": 75, "Drible": 65, "Defesa": 89, "Físico": 78},
    "Danilo": {"Ritmo": 76, "Finalização": 58, "Passe": 75, "Drible": 75, "Defesa": 81, "Físico": 80},
    "Marquinhos": {"Ritmo": 78, "Finalização": 45, "Passe": 75, "Drible": 74, "Defesa": 89, "Físico": 80},
    "Thiago Silva": {"Ritmo": 52, "Finalização": 54, "Passe": 73, "Drible": 72, "Defesa": 85, "Físico": 76},
    "Alex Sandro": {"Ritmo": 72, "Finalização": 62, "Passe": 75, "Drible": 76, "Defesa": 78, "Físico": 78},
    "Casemiro": {"Ritmo": 63, "Finalização": 73, "Passe": 79, "Drible": 72, "Defesa": 85, "Físico": 88},
    "Fred": {"Ritmo": 75, "Finalização": 68, "Passe": 78, "Drible": 80, "Defesa": 76, "Físico": 75},
    "Lucas Paquetá": {"Ritmo": 74, "Finalização": 76, "Passe": 82, "Drible": 85, "Defesa": 70, "Físico": 78},
    "Neymar": {"Ritmo": 86, "Finalização": 83, "Passe": 85, "Drible": 93, "Defesa": 37, "Físico": 61},
    "Richarlison": {"Ritmo": 81, "Finalização": 79, "Passe": 73, "Drible": 80, "Defesa": 52, "Físico": 78},
    "Gabriel Jesus": {"Ritmo": 83, "Finalização": 80, "Passe": 76, "Drible": 86, "Defesa": 40, "Físico": 74},

    # Holanda
    "Jasper Cillessen": {"Ritmo": 48, "Finalização": 25, "Passe": 65, "Drible": 60, "Defesa": 80, "Físico": 68},
    "Denzel Dumfries": {"Ritmo": 83, "Finalização": 65, "Passe": 72, "Drible": 75, "Defesa": 79, "Físico": 89},
    "Virgil van Dijk": {"Ritmo": 78, "Finalização": 60, "Passe": 71, "Drible": 72, "Defesa": 89, "Físico": 86},
    "Matthijs de Ligt": {"Ritmo": 66, "Finalização": 59, "Passe": 64, "Drible": 65, "Defesa": 85, "Físico": 86},
    "Daley Blind": {"Ritmo": 50, "Finalização": 62, "Passe": 82, "Drible": 76, "Defesa": 80, "Físico": 72},
    "Frenkie de Jong": {"Ritmo": 82, "Finalização": 69, "Passe": 86, "Drible": 87, "Defesa": 77, "Físico": 78},
    "Georginio Wijnaldum": {"Ritmo": 74, "Finalização": 74, "Passe": 78, "Drible": 82, "Defesa": 76, "Físico": 76},
    "Davy Klaassen": {"Ritmo": 68, "Finalização": 76, "Passe": 78, "Drible": 77, "Defesa": 72, "Físico": 76},
    "Steven Bergwijn": {"Ritmo": 85, "Finalização": 78, "Passe": 77, "Drible": 84, "Defesa": 40, "Físico": 74},
    "Donyell Malen": {"Ritmo": 89, "Finalização": 80, "Passe": 72, "Drible": 84, "Defesa": 35, "Físico": 72},
    "Memphis Depay": {"Ritmo": 81, "Finalização": 83, "Passe": 81, "Drible": 84, "Defesa": 30, "Físico": 79},

    # Alemanha
    "Manuel Neuer": {"Ritmo": 52, "Finalização": 25, "Passe": 78, "Drible": 65, "Defesa": 88, "Físico": 72},
    "Joshua Kimmich": {"Ritmo": 70, "Finalização": 72, "Passe": 87, "Drible": 83, "Defesa": 83, "Físico": 79},
    "Antonio Rüdiger": {"Ritmo": 82, "Finalização": 43, "Passe": 71, "Drible": 67, "Defesa": 86, "Físico": 86},
    "Niklas Süle": {"Ritmo": 70, "Finalização": 42, "Passe": 66, "Drible": 60, "Defesa": 83, "Físico": 83},
    "Robin Gosens": {"Ritmo": 80, "Finalização": 74, "Passe": 76, "Drible": 78, "Defesa": 77, "Físico": 82},
    "Ilkay Gündogan": {"Ritmo": 66, "Finalização": 80, "Passe": 86, "Drible": 85, "Defesa": 72, "Físico": 73},
    "Toni Kroos": {"Ritmo": 50, "Finalização": 81, "Passe": 90, "Drible": 81, "Defesa": 70, "Físico": 68},
    "Leon Goretzka": {"Ritmo": 78, "Finalização": 82, "Passe": 81, "Drible": 82, "Defesa": 80, "Físico": 86},
    "Serge Gnabry": {"Ritmo": 82, "Finalização": 84, "Passe": 80, "Drible": 85, "Defesa": 43, "Físico": 69},
    "Leroy Sané": {"Ritmo": 91, "Finalização": 81, "Passe": 80, "Drible": 86, "Defesa": 38, "Físico": 66},
    "Thomas Müller": {"Ritmo": 68, "Finalização": 84, "Passe": 83, "Drible": 80, "Defesa": 55, "Físico": 71},

    # Bélgica
    "Thibaut Courtois": {"Ritmo": 50, "Finalização": 20, "Passe": 65, "Drible": 60, "Defesa": 90, "Físico": 75},
    "Thomas Meunier": {"Ritmo": 74, "Finalização": 70, "Passe": 76, "Drible": 75, "Defesa": 78, "Físico": 82},
    "Toby Alderweireld": {"Ritmo": 52, "Finalização": 55, "Passe": 72, "Drible": 62, "Defesa": 82, "Físico": 80},
    "Jan Vertonghen": {"Ritmo": 54, "Finalização": 58, "Passe": 71, "Drible": 65, "Defesa": 81, "Físico": 78},
    "Timothy Castagne": {"Ritmo": 78, "Finalização": 65, "Passe": 74, "Drible": 76, "Defesa": 77, "Físico": 75},
    "Axel Witsel": {"Ritmo": 55, "Finalização": 70, "Passe": 80, "Drible": 76, "Defesa": 80, "Físico": 80},
    "Youri Tielemans": {"Ritmo": 65, "Finalização": 78, "Passe": 84, "Drible": 80, "Defesa": 70, "Físico": 72},
    "Kevin De Bruyne": {"Ritmo": 72, "Finalização": 85, "Passe": 94, "Drible": 87, "Defesa": 65, "Físico": 78},
    "Yannick Carrasco": {"Ritmo": 86, "Finalização": 78, "Passe": 80, "Drible": 86, "Defesa": 55, "Físico": 68},
    "Dries Mertens": {"Ritmo": 76, "Finalização": 82, "Passe": 80, "Drible": 85, "Defesa": 35, "Físico": 55},
    "Romelu Lukaku": {"Ritmo": 80, "Finalização": 85, "Passe": 72, "Drible": 75, "Defesa": 38, "Físico": 84},

    # Marrocos
    "Yassine Bounou": {"Ritmo": 50, "Finalização": 25, "Passe": 65, "Drible": 65, "Defesa": 85, "Físico": 70},
    "Achraf Hakimi": {"Ritmo": 92, "Finalização": 74, "Passe": 79, "Drible": 80, "Defesa": 76, "Físico": 78},
    "Romain Saïss": {"Ritmo": 58, "Finalização": 52, "Passe": 66, "Drible": 62, "Defesa": 80, "Físico": 82},
    "Nayef Aguerd": {"Ritmo": 68, "Finalização": 42, "Passe": 65, "Drible": 64, "Defesa": 81, "Físico": 80},
    "Noussair Mazraoui": {"Ritmo": 78, "Finalização": 66, "Passe": 79, "Drible": 81, "Defesa": 77, "Físico": 70},
    "Sofyan Amrabat": {"Ritmo": 65, "Finalização": 64, "Passe": 76, "Drible": 77, "Defesa": 78, "Físico": 85},
    "Azzedine Ounahi": {"Ritmo": 76, "Finalização": 68, "Passe": 78, "Drible": 82, "Defesa": 65, "Físico": 60},
    "Selim Amallah": {"Ritmo": 70, "Finalização": 72, "Passe": 74, "Drible": 76, "Defesa": 65, "Físico": 76},
    "Hakim Ziyech": {"Ritmo": 76, "Finalização": 78, "Passe": 85, "Drible": 83, "Defesa": 50, "Físico": 65},
    "Sofiane Boufal": {"Ritmo": 80, "Finalização": 72, "Passe": 75, "Drible": 85, "Defesa": 40, "Físico": 58},
    "Youssef En-Nesyri": {"Ritmo": 84, "Finalização": 82, "Passe": 65, "Drible": 74, "Defesa": 45, "Físico": 82}
}

def update_data_json():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for player in data['players']:
        if player['name'] in real_attributes:
            player['attributes'] = real_attributes[player['name']]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Atributos reais dos jogadores atualizados com sucesso no data.json!")

if __name__ == '__main__':
    update_data_json()
