import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

segredo = json.loads(os.getenv('API_KEY'))
key = segredo["key"]

url = 'https://api.waifu.im/images'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    image_url = data['items'][0]['url']
    
    os.makedirs('images', exist_ok=True)
    
    filename = image_url.split('/')[-1]
    filepath = os.path.join('images', filename)
    
    image_response = requests.get(image_url)
    with open(filepath, 'wb') as f:
        f.write(image_response.content)
    
    print(f"Imagem salva em: {filepath}")
else:
    print(f"Erro: {response.status_code}")