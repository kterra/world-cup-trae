from flask import Flask, render_template, request, jsonify
import json

import feedparser
import urllib.parse
from datetime import datetime
import ssl

# Fix para erro de certificado SSL no feedparser (Mac)
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

def get_player_news(player_name, country):
    query = urllib.parse.quote(f"{player_name} {country} football")
    url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    try:
        feed = feedparser.parse(url)
        news = []
        for entry in feed.entries[:5]:
            # Limpar data
            try:
                dt = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                date_str = dt.strftime("%d/%m/%Y")
            except:
                date_str = entry.published
                
            news.append({
                "title": entry.title,
                "url": entry.link,
                "source": entry.source.title if hasattr(entry, 'source') else "Notícia",
                "date": date_str
            })
        return news
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return []

# Carregar dados locais
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    data = load_data()
    country_filter = request.args.get('country')
    wc_year = request.args.get('wc_year')
    sort_by = request.args.get('sort_by', 'default')
    
    players = data['players']
    
    # Extrair todos os anos de copas do mundo disponíveis para o filtro
    all_wc_years = sorted(list(set(year for p in players for year in p.get('world_cups', []))), reverse=True)
    
    if country_filter:
        players = [p for p in players if p['country'] == country_filter]
        
    if wc_year:
        players = [p for p in players if wc_year in p.get('world_cups', [])]
        
    if sort_by == 'caps_desc':
        players.sort(key=lambda x: x.get('caps_since_2018', 0), reverse=True)
    elif sort_by == 'caps_asc':
        players.sort(key=lambda x: x.get('caps_since_2018', 0))
    elif sort_by == 'wc_desc':
        players.sort(key=lambda x: len(x.get('world_cups', [])), reverse=True)
    elif sort_by == 'wc_asc':
        players.sort(key=lambda x: len(x.get('world_cups', [])))
        
    return render_template(
        'index.html', 
        teams=data['teams'], 
        players=players, 
        selected_country=country_filter,
        selected_wc_year=wc_year,
        selected_sort=sort_by,
        wc_years=all_wc_years
    )

@app.route('/player/<player_id>')
def player_profile(player_id):
    data = load_data()
    player = next((p for p in data['players'] if p['id'] == player_id), None)
    
    if not player:
        return "Jogador não encontrado", 404
        
    # Fetch real-time news
    player['news'] = get_player_news(player['name'], player['country'])
    
    # Preparar lista de outros jogadores para o duelo
    other_players = [p for p in data['players'] if p['id'] != player_id]
        
    return render_template('profile.html', player=player, other_players=other_players)

@app.route('/duel/<player1_id>/<player2_id>')
def player_duel(player1_id, player2_id):
    data = load_data()
    player1 = next((p for p in data['players'] if p['id'] == player1_id), None)
    player2 = next((p for p in data['players'] if p['id'] == player2_id), None)
    
    if not player1 or not player2:
        return "Um ou ambos os jogadores não foram encontrados", 404
        
    return render_template('duel.html', p1=player1, p2=player2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
