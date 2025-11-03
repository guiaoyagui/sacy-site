import requests
import json
import sys
import time
from ddgs import DDGS # Vamos manter para buscar imagens

# --- Configuração da API do Gemini ---
# (Deixe a apiKey em branco, o Canvas/Google a fornecerá)
API_KEY = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

# O "prompt do sistema" que define a personalidade e a tarefa da IA.
# Isto substitui a sua função _gerar_resumo() com muito mais poder.
SYSTEM_PROMPT = """
Você é Sacy, um assistente de IA educacional e amigável.
Sua tarefa é responder consultas de estudantes. 
Use a ferramenta de busca (Google Search) para encontrar as informações mais relevantes.
Com base nos resultados da busca, escreva um resumo didático, claro, conciso e em português (do Brasil) sobre o tópico solicitado.
O resumo deve ser ideal para um estudante (evite jargões complexos).
Não inclua o título no seu resumo, apenas o texto principal.
"""

class AgentPesquisa:
    
    def __init__(self):
        """Inicializa o agente com o DDGS (apenas para imagens)."""
        self.ddgs = DDGS()
        self.session = requests.Session() # Reutiliza a sessão para performance

    def _buscar_imagens(self, consulta: str) -> list:
        """
        Busca imagens usando DDGS.
        (Esta é a sua função original, que é boa para imagens).
        """
        imagens = []
        try:
            for img in self.ddgs.images(consulta, max_results=5):
                url = img.get("image")
                if url and url.startswith("http"):
                    imagens.append(url)
                if len(imagens) >= 3:
                    return imagens
        except Exception as e:
            print(f"⚠️ Erro ao buscar imagens no DDGS: {e}", file=sys.stderr)
        
        return imagens[:3]

    def buscar_e_resumir(self, consulta: str) -> dict:
        """
        Busca na web usando a API do Gemini (Google AI) e resume.
        Retorna um dicionário com dados estruturados (JSON).
        """
        
        # --- Passo 1: Construir o Payload da API ---
        payload = {
            "contents": [{
                "parts": [{"text": consulta}]
            }],
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            # --- Este é o segredo! ---
            # Habilita a ferramenta de Google Search para "aterrar" (grounding)
            # a resposta da IA em fatos da web.
            "tools": [{
                "google_search": {}
            }],
        }

        # --- Passo 2: Chamar a API com Retentativa (Backoff) ---
        max_retries = 3
        delay = 1
        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    API_URL, 
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload),
                    timeout=45 # Aumentar o timeout para IA generativa
                )
                
                response.raise_for_status() # Levanta erro para 4xx/5xx
                
                # --- Passo 3: Processar a Resposta ---
                result = response.json()
                
                candidate = result.get('candidates', [{}])[0]
                content = candidate.get('content', {}).get('parts', [{}])[0]
                
                # 1. Extrair o Resumo (o texto gerado pela IA)
                resumo_ia = content.get('text', '')
                
                if not resumo_ia:
                    print("⚠️ IA não retornou resumo.", file=sys.stderr)
                    resumo_ia = "Não foi possível gerar um resumo. Tente novamente."

                # 2. Extrair as Fontes (do GroundingMetadata)
                fontes = []
                metadata = candidate.get('groundingMetadata', {})
                if 'groundingAttributions' in metadata:
                    for attr in metadata.get('groundingAttributions', []):
                        if 'web' in attr:
                            fontes.append({
                                "url": attr['web'].get('uri'),
                                "titulo": attr['web'].get('title', 'Fonte')
                            })

                # 3. Buscar Imagens (usando nosso método _buscar_imagens)
                imagens = self._buscar_imagens(consulta)
                
                # 4. Retornar JSON Limpo
                return {
                    "consulta": consulta,
                    "resumo": resumo_ia,
                    "fontes": fontes,
                    "imagens": imagens
                }

            except requests.exceptions.HTTPError as http_err:
                print(f"❌ Erro HTTP (Tentativa {attempt+1}): {http_err}", file=sys.stderr)
                # Tenta ler a resposta de erro da API
                try:
                    print(f"Detalhe do Erro: {response.text}", file=sys.stderr)
                except:
                    pass

                if response.status_code == 429 or response.status_code >= 500:
                    # 429 (Rate Limit) ou 5xx (Server Error) -> Tentar de novo
                    time.sleep(delay)
                    delay *= 2 # Backoff exponencial
                else:
                    # Erro 400 (Bad Request) - não adianta tentar de novo
                    return {"erro": f"Erro na requisição: {http_err}"}
            
            except requests.exceptions.RequestException as req_err:
                # Erros de conexão, timeout, etc.
                print(f"❌ Erro de Conexão (Tentativa {attempt+1}): {req_err}", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
            
            except Exception as e:
                print(f"❌ Erro inesperado ao processar API: {e}", file=sys.stderr)
                return {"erro": f"Erro inesperado no processamento: {str(e)}"}

        # Se todas as tentativas falharem
        return {"erro": "Não foi possível conectar à API de IA após várias tentativas."}

# --- Bloco para teste local ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        consulta_teste = " ".join(sys.argv[1:])
    else:
        consulta_teste = "Revolução Francesa"
        
    print(f"--- Testando Agente de Pesquisa (Gemini API) ---")
    print(f"Buscando por: {consulta_teste}...")
    
    agent = AgentPesquisa()
    resultado = agent.buscar_e_resumir(consulta_teste)
    
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

