import requests
import sys
import json

def buscar_na_wikipedia(consulta):
    """
    Busca um resumo na Wikipedia usando a API oficial REST_v1.
    Isso substitui o método anterior de web scraping (com BeautifulSoup), 
    que era instável e sujeito a quebras.
    """ 
    
    # Prepara a URL da API da Wikipedia.
    # A API é sensível a maiúsculas/minúsculas e espera espaços como "_" (underscores).
    consulta_formatada = consulta.replace(" ", "_")
    
    # --- Ponto principal do Upgrade 1 ---
    # Usamos a API em português (pt.wikipedia.org) para melhores resultados locais.
    url_api = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{consulta_formatada}"
    
    # Define um User-Agent amigável.
    # A API da Wikipedia recomenda/exige um User-Agent para evitar bloqueios.
    headers = {
        'User-Agent': 'SacyAI/1.0 (sacy-ai-bot@example.com)' # Um User-Agent de exemplo
    }
    
    try:
        response = requests.get(url_api, headers=headers)
        
        # Verifica se a página foi encontrada (ex: 404) ou outros erros
        response.raise_for_status() 
        
        data = response.json()
        
        # Extrai os dados limpos do JSON
        titulo = data.get('title', 'Título não encontrado')
        resumo = data.get('extract', 'Resumo não disponível.')
        
        # A imagem principal (thumbnail)
        imagem_url = data.get('thumbnail', {}).get('source', None)
        
        # Link para a página original
        link_artigo = data.get('content_urls', {}).get('desktop', {}).get('page', url_api)
        
        # Retorna os dados estruturados (JSON limpo)
        return {
            "titulo": titulo,
            "resumo": resumo,
            "imagem_url": imagem_url,
            "fonte": link_artigo
        }

    except requests.exceptions.HTTPError as http_err:
        # Se a página não for encontrada (404), retorna um erro amigável
        if response.status_code == 404:
            return {
                "erro": f"Desculpe, não consegui encontrar um artigo na Wikipedia para '{consulta}'."
            }
        else:
            # Outros erros de servidor (500, 503, etc.)
            return {
                "erro": f"Erro HTTP ao buscar na Wikipedia: {http_err}"
            }
    except requests.exceptions.RequestException as req_err:
        # Erros de conexão (DNS, rede, etc.)
        return {
            "erro": f"Erro de conexão ao buscar na Wikipedia: {req_err}"
        }
    except Exception as e:
        # Pega qualquer outro erro inesperado
        return {
            "erro": f"Um erro inesperado ocorreu ao processar sua busca: {e}"
        }

# --- Bloco para teste local ---
# Se este script for executado diretamente (ex: "python agent_literatura.py 'Machado de Assis'"),
# ele fará uma busca de teste e imprimirá o resultado.
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Pega a consulta dos argumentos da linha de comando
        consulta_teste = " ".join(sys.argv[1:])
    else:
        # Se nenhum argumento for dado, usa uma consulta padrão
        consulta_teste = "Inteligência artificial"
        
    print(f"--- Testando Agente de Literatura (Wikipedia API) ---")
    print(f"Buscando por: {consulta_teste}...")
    
    resultado = buscar_na_wikipedia(consulta_teste)
    
    # Imprime o resultado formatado (pretty print)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

