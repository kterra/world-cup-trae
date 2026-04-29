import json
import urllib.parse
import urllib.request
import ssl

def get_wiki_image(name):
    try:
        # Usando urllib para evitar problemas de certificado
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
    except Exception as e:
        print(f"Error fetching image for {name}: {e}")
    return "https://ui-avatars.com/api/?name=" + name.replace(" ", "+") + "&size=500&background=0f172a&color=38bdf8"

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data['players']:
    print(f"Fetching {p['name']}...")
    p['photo_url'] = get_wiki_image(p['name'])

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Updated images.")
