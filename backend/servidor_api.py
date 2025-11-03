import os
import json
import re
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from markdown import markdown # Importa o conversor de Markdown

# --- Correção do Import (Upgrade 1) ---
from agent_literatura import buscar_na_wikipedia

# --- Import do Novo Agente (Upgrade 2) ---
from agent_pesquisa import AgentPesquisa

# --- Import dos Agentes ENEM (Upgrade 3) ---
from agentes_especializados import (
    agente_modo_exatas, 
    agente_modo_arte_placeholder,
    agente_modo_literatura_placeholder,
    agente_modo_quimica_placeholder,
    agente_modo_geografia_placeholder,
    agente_modo_redacao # <-- CORREÇÃO: Importa a função real
)

# --- Configuração do Servidor ---
app = Flask(__name__)
CORS(app) # Permite que o seu frontend chame esta API

# Inicializa o agente de pesquisa (IA)
agent_web = AgentPesquisa()

# --- NOVO: Configuração do Cliente Gemini para Classificação ---
try:
    # (Deixe a apiKey em branco, o Canvas/Google a fornecerá)
    API_KEY = "" 
    if not API_KEY:
        API_KEY = os.environ.get("GEMINI_API_KEY") # Tenta ler do ambiente

    genai.configure(api_key=API_KEY)
    model_classifier = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    print("🤖 Cliente Gemini (Classificador) configurado com sucesso.")
except Exception as e:
    print(f"❌ ERRO GRAVE: Falha ao configurar o cliente Gemini (Classificador). Verifique a API_KEY. Erro: {e}")
    model_classifier = None
# --- FIM DA CONFIGURAÇÃO ---


@app.route("/")
def health_check():
    """Verifica se a API está online."""
    return jsonify({"status": "online", "message": "Sacy API está no ar!"})


@app.route("/wikipedia")
def endpoint_wikipedia():
    """
    Endpoint para buscar na Wikipedia.
    Ex: /wikipedia?q=Machado+de+Assis
    """
    consulta = request.args.get('q')
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' (consulta) é obrigatório."}), 400

    # 1. Obter DADOS (JSON) do agente
    print(f"Buscando [Wikipedia] por: {consulta}...")
    dados = buscar_na_wikipedia(consulta)
    
    if "erro" in dados:
        return jsonify(dados), 404 # Retorna o erro como JSON

    # 2. Formatar DADOS em HTML (Apresentação para o Sacy)
    imagem_html = ""
    if dados.get('imagem_url'):
        imagem_html = f"""
        <img src='{dados['imagem_url']}' alt='{dados['titulo']}' 
             style='width:120px; height:140px; object-fit:cover; border-radius:10px; 
                    float:right; margin-left:15px; border: 2px solid #555;'>
        """

    html_resposta = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #555; border-radius:15px; padding:20px; background-color:#1e293b;'>
        <h2 style='color:#a5b4fc; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/ffffff/a5b4fc?text=W' width='30' height='30' alt='Wikipedia' style='border-radius: 4px;'>
            {dados['titulo']} (Wikipedia)
        </h2>
        <div style='clear:both; padding-top:10px;'>
            {imagem_html}
            <p style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify;'>
                {dados['resumo']}
            </p>
        </div>
        <a href='{dados['fonte']}' target='_blank' style='display:inline-block; margin-top:15px; color:#7dd3fc;
           text-decoration:none; font-weight:500; font-size:14px;'>
           📘 Ler artigo completo na Wikipedia
        </a>
    </div>
    """
    return html_resposta


@app.route("/pesquisar")
def endpoint_pesquisa_ia():
    """
    Endpoint para a pesquisa principal (Web + Gemini IA).
    Ex: /pesquisar?q=Revolucao+Francesa
    """
    consulta = request.args.get('q')
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' (consulta) é obrigatório."}), 400

    # 1. Obter DADOS (JSON) do agente
    print(f"Buscando [Web IA] por: {consulta}...")
    dados = agent_web.buscar_e_resumir(consulta)

    if "erro" in dados:
        return jsonify(dados), 500 # Retorna o erro como JSON

    # 2. Formatar DADOS em HTML (Apresentação para o Sacy)
    
    # --- CORREÇÃO: Formatar Resumo (Markdown -> HTML) ---
    # Usamos a biblioteca 'markdown' para converter o texto da IA
    resumo_html = markdown(dados.get('resumo', ''))
    
    # --- CORREÇÃO: Link da Matéria (Fonte) ---
    # Substituindo a lista de fontes por um link de pesquisa
    link_google = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
    fontes_html = f"""
    <a href='{link_google}' target='_blank' style='display:inline-block; margin-top:15px; color:#7dd3fc;
       text-decoration:none; font-weight:500; font-size:14px;'>
       📘 Pesquisar este tópico no Google
    </a>
    """
    
    # --- CORREÇÃO: Formatar imagens (Maiores) ---
    imagens_html = ""
    imagens_lista = dados.get('imagens', [])
    if imagens_lista:
        for img_url in imagens_lista[:3]: # Limitar a 3 imagens
            # Aumentamos o tamanho da imagem e o espaçamento
            imagens_html += f"""
            <img src='{img_url}' alt='{consulta}' 
                 style='width: 300px; height: 200px; object-fit:cover; margin:4px; 
                        border-radius:8px; border: 1px solid #444;'>
            """
    else:
        imagens_html = "<p style='color:#999; font-size:14px;'>Nenhuma imagem de apoio encontrada.</p>"

    # Montar o card de resposta final
    html_resposta = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #555; border-radius:15px; padding:20px; background-color:#1e293b;'>
        <h2 style='color:#7dd3fc; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/28x28/ffffff/7dd3fc?text=G' width='28' height='28' alt='Google Search' style='border-radius: 4px;'>
            Resumo Educacional (Sacy IA)
        </h2>
        <p style='font-size:15px; margin-top:4px; color:#ccc;'><b>Tópico:</b> {dados['consulta']}</p>
        
        <h3 style='color:#93c5fd; margin-top:10px; margin-bottom: 6px; font-size:16px;'>📄 Resumo</h3>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify;'>
            {resumo_html}
        </div>

        {fontes_html}

        <hr style='margin:20px 0 15px 0; border: 0; border-top: 1px solid #334155;'>

        <h3 style='color:#7dd3fc; margin-bottom:10px; font-size:16px;'>🖼️ Imagens relacionadas:</h3>
        <div style='display:flex; flex-wrap:wrap; gap:20px; justify-content:center;'>
            {imagens_html}
        </div>
    </div>
    """
    return html_resposta


# --- NOVO ENDPOINT: MODO FOCO ENEM ---
@app.route("/pesquisar-enem")
def endpoint_pesquisa_enem():
    """
    Endpoint inteligente para o Modo Foco ENEM.
    Ele classifica a consulta e chama o agente especializado correto.
    """
    consulta = request.args.get('q')
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' (consulta) é obrigatório."}), 400
    
    if not model_classifier:
        return jsonify({"erro": "O modelo classificador (Gemini) não foi inicializado."}), 500

    print(f"\n[ROTEADOR ENEM] Classificando consulta: '{consulta}'...")

    # --- PASSO 1: Classificar a consulta ---
    try:
        # Este é o prompt do "cérebro" classificador
        prompt_classificador = f"""
        Analise a consulta do usuário e classifique-a em UMA das seguintes categorias:
        [MATEMATICA, FISICA, QUIMICA, GEOGRAFIA, LITERATURA, ARTE, REDACAO, HISTORIA, BIOLOGIA, OUTRO]
        
        Sua resposta DEVE ser apenas a palavra da categoria, em maiúsculas.
        
        Exemplos:
        Consulta: "Quem foi Tarsila do Amaral?" -> ARTE
        Consulta: "fórmula de bhaskara" -> MATEMATICA
        Consulta: "O que é uma célula eucarionte?" -> BIOLOGIA
        Consulta: "Como funciona uma pilha?" -> QUIMICA
        Consulta: "Ajude-me a corrigir esta redação..." -> REDACAO
        Consulta: "Revolução Francesa" -> HISTORIA
        Consulta: "Climas do Brasil" -> GEOGRAFIA
        Consulta: "Qual o melhor time de futebol?" -> OUTRO
        
        Consulta para classificar: "{consulta}"
        """
        
        response = model_classifier.generate_content(prompt_classificador)
        categoria = response.text.strip().upper()
        
        # Validação simples
        valid_categories = ["MATEMATICA", "FISICA", "QUIMICA", "GEOGRAFIA", "LITERATURA", "ARTE", "REDACAO", "HISTORIA", "BIOLOGIA", "OUTRO"]
        if categoria not in valid_categories:
            print(f"[ROTETEADOR ENEM] Classificação falhou ou retornou inesperado: '{categoria}'. Usando 'OUTRO'.")
            categoria = "OUTRO"
            
        print(f"[ROTEADOR ENEM] Consulta classificada como: {categoria}")

    except Exception as e:
        print(f"❌ Erro ao classificar consulta: {e}")
        # Se a classificação falhar, apenas faça uma pesquisa normal
        categoria = "OUTRO"

    # --- PASSO 2: Rotear para o Agente Correto ---
    
    # Se for Mat/Fis, usa o agente de Exatas
    if categoria in ["MATEMATICA", "FISICA"]:
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_exatas")
        return agente_modo_exatas(consulta, categoria)
        
    # Se for Arte, usa o placeholder de Arte
    elif categoria == "ARTE":
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_arte_placeholder")
        return agente_modo_arte_placeholder(consulta)
        
    # Se for Literatura, usa o placeholder de Literatura
    elif categoria == "LITERATURA":
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_literatura_placeholder")
        return agente_modo_literatura_placeholder(consulta)
        
    # Se for Química, usa o placeholder de Química
    elif categoria == "QUIMICA":
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_quimica_placeholder")
        return agente_modo_quimica_placeholder(consulta)
        
    # Se for Geografia, usa o placeholder de Geografia
    elif categoria == "GEOGRAFIA":
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_geografia_placeholder")
        return agente_modo_geografia_placeholder(consulta)
        
    # Se for Redação, usa o placeholder de Redação
    elif categoria == "REDACAO":
        print(f"[ROTEADOR ENEM] Roteando para: agente_modo_redacao")
        return agente_modo_redacao(consulta)
        
    # Se for "OUTRO" ou qualquer outra matéria (História, Biologia, etc.)
    # apenas fazemos uma pesquisa normal com o /pesquisar
    else:
        print(f"[ROTEADOR ENEM] Categoria '{categoria}' não tem agente. Usando /pesquisar padrão.")
        return endpoint_pesquisa_ia()


# --- Bloco para executar o servidor ---
if __name__ == "__main__":
    # Para rodar, você precisará ter as bibliotecas:
    # pip install Flask flask-cors markdown google-generativeai
    print("🚀 Iniciando servidor Sacy API em http://127.0.0.1:5000")
    print("Rotas disponíveis:")
    print("   /wikipedia?q=...")
    print("   /pesquisar?q=...")
    print("   /pesquisar-enem?q=...") # <-- A NOVA ROTA
    app.run(debug=True, port=5000)


