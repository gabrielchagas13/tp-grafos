"""
Script para verificar o status do rate limit do GitHub
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

def check_rate_limit():
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=headers)
        data = response.json()
        
        core = data['resources']['core']
        
        print("="*50)
        print("STATUS DO RATE LIMIT")
        print("="*50)
        print(f"Token configurado: {'Sim' if token else 'Não'}")
        print(f"Requests restantes: {core['remaining']}")
        print(f"Limite total: {core['limit']}")
        print(f"Reset em: {datetime.fromtimestamp(core['reset'])}")
        
        if core['remaining'] == 0:
            wait_time = core['reset'] - int(datetime.now().timestamp())
            print(f"\n🚨 RATE LIMIT ESGOTADO!")
            print(f"Aguarde {wait_time//60} minutos e {wait_time%60} segundos")
        elif core['remaining'] < 100:
            print(f"\n⚠️  Poucos requests restantes: {core['remaining']}")
        else:
            print(f"\n✅ Rate limit OK: {core['remaining']} requests disponíveis")
            
    except Exception as e:
        print(f"Erro ao verificar rate limit: {e}")

if __name__ == "__main__":
    check_rate_limit()