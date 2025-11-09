"""
Extração de Dados - MMDetection
Trabalho de Teoria dos Grafos - Etapa 1

Este script executa APENAS a extração de dados do repositório 
open-mmlab/mmdetection via API do GitHub, salvando os dados 
em arquivos CSV para posterior análise de grafos.
"""

import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Execução da extração de dados"""
    
    print("="*60)
    print("EXTRAÇÃO DE DADOS - MMDETECTION")
    print("Trabalho de Teoria dos Grafos - Etapa 1")
    print("="*60)
    
    # Carrega configurações
    load_dotenv()
    
    # Configurações
    REPO_OWNER = os.getenv('REPO_OWNER', 'open-mmlab')
    REPO_NAME = os.getenv('REPO_NAME', 'mmdetection')
    MAX_ISSUES = int(os.getenv('MAX_ISSUES', 500))
    MAX_PRS = int(os.getenv('MAX_PRS', 500))
    
    print(f"Repositório: {REPO_OWNER}/{REPO_NAME}")
    print(f"Máximo de issues: {MAX_ISSUES}")
    print(f"Máximo de PRs: {MAX_PRS}")
    print()
    
    # Inicializa o extrator de dados
    from src.github_extractor import GitHubDataExtractor
    
    try:
        # ETAPA 1: EXTRAÇÃO DE DADOS DO GITHUB
        print("ETAPA 1: Extração de dados do GitHub")
        print("-" * 50)
        
        # Inicializa o extrator
        extractor = GitHubDataExtractor(REPO_OWNER, REPO_NAME)
        
        # Tenta extrair dados do GitHub
        try:
            print(f"Iniciando extração do repositório {REPO_OWNER}/{REPO_NAME}...")
            data = extractor.extract_all_data(MAX_ISSUES, MAX_PRS)
            print("\n✓ Dados extraídos com sucesso do GitHub!")
        except Exception as e:
            print(f"\n✗ Erro ao extrair do GitHub: {e}")
            print("\nVerifique:")
            print("1. Token do GitHub configurado no arquivo .env")
            print("2. Conexão com a internet")
            print("3. Rate limit da API GitHub")
            return 1
        
        # RESUMO DOS DADOS EXTRAÍDOS
        print("\n" + "="*50)
        print("RESUMO DOS DADOS EXTRAÍDOS")
        print("="*50)
        
        total_records = 0
        for key, df in data.items():
            count = len(df)
            total_records += count
            print(f"✓ {key.replace('_', ' ').title()}: {count} registros")
        
        print(f"\n📊 TOTAL: {total_records} registros extraídos")
        
        # ARQUIVOS GERADOS
        print("\n📁 ARQUIVOS SALVOS NA PASTA 'data/':")
        print("-" * 30)
        data_files = [f for f in os.listdir('data') if f.endswith('.csv')]
        for file in data_files:
            print(f"  • {file}")
        
        # PRÓXIMOS PASSOS
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("-" * 20)
        print("1. Os dados estão prontos para construção dos grafos")
        print("2. Execute a Etapa 2 para modelagem dos grafos")
        print("3. Use os arquivos CSV para análises personalizadas")
        print("4. Implemente algoritmos de análise de grafos")
        
        print(f"\n✅ ETAPA 1 CONCLUÍDA COM SUCESSO!")
        print("� Dados do repositório extraídos e salvos em CSV")
        print("="*50)
        
    except Exception as e:
        print(f"\n✗ ERRO NA EXTRAÇÃO: {e}")
        print("\nVerifique:")
        print("1. Token do GitHub configurado no arquivo .env")
        print("2. Conexão com a internet")
        print("3. Rate limit da API GitHub")
        print("4. Dependências instaladas (requirements.txt)")
        
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)