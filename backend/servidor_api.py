import os
import json
import re
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from markdown import markdown  # Importa o conversor de Markdown

# --- Correção do Import (Upgrade 1) ---
from agent_literatura import buscar_na_wikipedia

# --- Import do Novo Agente (Upgrade 2) ---
from agent_pesquisa import AgentPesquisa

# --- Import dos Agentes ENEM (Upgrade 3) ---
from agentes_especializados import (
    agente_modo_exatas,
    agente_modo_arte_placeholder,
    agente_modo_literatura,          # ✅ agora importando o agente REAL
    agente_modo_quimica,             # ✅ agora importando o agente REAL
    agente_modo_geografia,           # ✅ agora importando o agente REAL
    agente_modo_redacao
)

# --- Configuração do Servidor ---
app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

# Inicializa o agente de pesquisa (IA)
agent_web = AgentPesquisa()

# --- NOVO: Configuração do Cliente Gemini para Classificação ---
try:
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        API_KEY = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4"

    genai.configure(api_key=API_KEY)
    model_classifier = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    print("🤖 Cliente Gemini (Classificador) configurado com sucesso.")
except Exception as e:
    print(f"❌ ERRO GRAVE: Falha ao configurar o cliente Gemini (Classificador). Erro: {e}")
    model_classifier = None


@app.route("/")
def health_check():
    return jsonify({"status": "online", "message": "Sacy API está no ar!"})


@app.route("/wikipedia")
def endpoint_wikipedia():
    consulta = request.args.get("q")
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' é obrigatório."}), 400

    print(f"Buscando [Wikipedia] por: {consulta}...")
    dados = buscar_na_wikipedia(consulta)

    if "erro" in dados:
        return jsonify(dados), 404

    imagem_html = ""
    if dados.get("imagem_url"):
        imagem_html = f"""
        <img src='{dados['imagem_url']}' alt='{dados['titulo']}' 
             style='width:120px; height:140px; object-fit:cover; border-radius:10px; 
                    float:right; margin-left:15px; border: 2px solid #555;'>
        """

    html_resposta = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border:1px solid #555; border-radius:15px; padding:20px; background-color:#1e293b;'>
        <h2 style='color:#a5b4fc; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/ffffff/a5b4fc?text=W' width='30' height='30'>
            {dados['titulo']} (Wikipedia)
        </h2>
        <div style='clear:both; padding-top:10px;'>
            {imagem_html}
            <p style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify;'>
                {dados['resumo']}
            </p>
        </div>
        <a href='{dados['fonte']}' target='_blank' style='display:inline-block; margin-top:15px; color:#7dd3fc; text-decoration:none; font-weight:500; font-size:14px;'>
           📘 Ler artigo completo na Wikipedia
        </a>
    </div>
    """
    return html_resposta


@app.route("/pesquisar")
def endpoint_pesquisa_ia():
    consulta = request.args.get("q")
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' é obrigatório."}), 400

    print(f"Buscando [Web IA] por: {consulta}...")
    dados = agent_web.buscar_e_resumir(consulta)

    if "erro" in dados:
        return jsonify(dados), 500

    resumo_html = markdown(dados.get("resumo", ""))
    link_google = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
    fontes_html = f"""
    <a href='{link_google}' target='_blank' style='display:inline-block; margin-top:15px; color:#7dd3fc;
       text-decoration:none; font-weight:500; font-size:14px;'>
       📘 Pesquisar este tópico no Google
    </a>
    """

    imagens_html = ""
    imagens_lista = dados.get("imagens", [])
    if imagens_lista:
        for img_url in imagens_lista[:3]:
            imagens_html += f"""
            <img src='{img_url}' alt='{consulta}' 
                 style='width: 300px; height: 200px; object-fit:cover; margin:4px; 
                        border-radius:8px; border: 1px solid #444;'>
            """
    else:
        imagens_html = "<p style='color:#999; font-size:14px;'>Nenhuma imagem de apoio encontrada.</p>"

    html_resposta = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border:1px solid #555; border-radius:15px; padding:20px; background-color:#1e293b;'>
        <h2 style='color:#7dd3fc; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/28x28/ffffff/7dd3fc?text=G' width='28' height='28'>
            Resumo Educacional (Sacy IA)
        </h2>
        <p style='font-size:15px; margin-top:4px; color:#ccc;'><b>Tópico:</b> {dados['consulta']}</p>
        <h3 style='color:#93c5fd; margin-top:10px; margin-bottom:6px; font-size:16px;'>📄 Resumo</h3>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify;'>
            {resumo_html}
        </div>
        {fontes_html}
        <hr style='margin:20px 0 15px 0; border:0; border-top:1px solid #334155;'>
        <h3 style='color:#7dd3fc; margin-bottom:10px; font-size:16px;'>🖼️ Imagens relacionadas:</h3>
        <div style='display:flex; flex-wrap:wrap; gap:20px; justify-content:center;'>
            {imagens_html}
        </div>
    </div>
    """
    return html_resposta


@app.route("/pesquisar-enem")
def endpoint_pesquisa_enem():
    consulta = request.args.get("q")
    if not consulta:
        return jsonify({"erro": "Parâmetro 'q' é obrigatório."}), 400

    if not model_classifier:
        return jsonify({"erro": "O modelo classificador não foi inicializado."}), 500

    print(f"\n[ROTEADOR ENEM] Classificando consulta: '{consulta}'...")

    try:
        prompt_classificador = f"""
        Analise a consulta do usuário e classifique-a em UMA das seguintes categorias:
        [MATEMATICA, FISICA, QUIMICA, GEOGRAFIA, LITERATURA, ARTE, REDACAO, HISTORIA, BIOLOGIA, OUTRO]

        Responda apenas com a categoria em letras maiúsculas.
        Consulta: "{consulta}"
        """
        response = model_classifier.generate_content(prompt_classificador)
        categoria = response.text.strip().upper()

        valid_categories = ["MATEMATICA", "FISICA", "QUIMICA", "GEOGRAFIA", "LITERATURA", "ARTE", "REDACAO", "HISTORIA", "BIOLOGIA", "OUTRO"]
        if categoria not in valid_categories:
            print(f"[ROTEADOR ENEM] Categoria inesperada '{categoria}', usando OUTRO.")
            categoria = "OUTRO"

        print(f"[ROTEADOR ENEM] Consulta classificada como: {categoria}")
    except Exception as e:
        print(f"❌ Erro ao classificar consulta: {e}")
        categoria = "OUTRO"

    # --- PASSO 2: Roteamento ---
    if categoria in ["MATEMATICA", "FISICA"]:
        return agente_modo_exatas(consulta, categoria)
    elif categoria == "ARTE":
        return agente_modo_arte_placeholder(consulta)
    elif categoria == "LITERATURA":
        return agente_modo_literatura(consulta)
    elif categoria == "QUIMICA":
        return agente_modo_quimica(consulta)
    elif categoria == "GEOGRAFIA":
        return agente_modo_geografia(consulta)
    elif categoria == "REDACAO":
        return agente_modo_redacao(consulta)
    else:
        return endpoint_pesquisa_ia()


# --- ✅ NOVO ENDPOINT: GERAR QUIZ ---
@app.route("/gerar-quiz", methods=["POST"])
def gerar_quiz():
    """
    Gera 3 perguntas de múltipla escolha baseadas no texto recebido.
    Retorna JSON no formato:
    { "quiz": [ { "pergunta": "...", "alternativas": [...], "correta": 0 } ] }
    """
    data = request.get_json()
    texto_base = data.get("texto")

    if not texto_base:
        return jsonify({"erro": "Campo 'texto' é obrigatório."}), 400

    try:
        sys_prompt = """
        Você é Sacy, um criador de quizzes educacionais para estudantes do ENEM.
        Gere exatamente 3 perguntas de múltipla escolha sobre o texto fornecido.
        Retorne APENAS um JSON válido no formato:
        {
          "quiz": [
            {
              "pergunta": "string",
              "alternativas": ["A", "B", "C", "D"],
              "correta": 0
            }
          ]
        }
        NÃO escreva nada fora do JSON.
        """

        prompt_completo = f"{sys_prompt}\n\nTexto base:\n{texto_base}"

        response = model_classifier.generate_content(prompt_completo)
        resposta_texto = response.text.strip()

        match = re.search(r"\{[\s\S]*\}", resposta_texto)
        if not match:
            return jsonify({"erro": "Não foi possível extrair JSON válido da IA."}), 500

        quiz_json = json.loads(match.group(0))
        return jsonify(quiz_json)

    except Exception as e:
        print(f"❌ Erro ao gerar quiz: {e}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500


if __name__ == "__main__":
    print("🚀 Iniciando servidor Sacy API em http://127.0.0.1:5000")
    print("Rotas disponíveis:")
    print("   /wikipedia?q=...")
    print("   /pesquisar?q=...")
    print("   /pesquisar-enem?q=...")
    print("   /gerar-quiz  [POST]")
    app.run(debug=True, port=5000)
