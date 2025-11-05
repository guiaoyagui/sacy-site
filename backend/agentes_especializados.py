import os
import json
import google.generativeai as genai
from markdown import markdown

# --- Configuração do Cliente Gemini ---
try:
    API_KEY = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4"
    if not API_KEY:
        API_KEY = os.environ.get("GEMINI_API_KEY")

    genai.configure(api_key=API_KEY)
    model_agent = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    print("🤖 Cliente Gemini (Agentes) configurado com sucesso.")
except Exception as e:
    print(f"❌ ERRO GRAVE: Falha ao configurar o cliente Gemini (Agentes). Erro: {e}")
    model_agent = None


# ============================================================
# 🧮 AGENTE 1: EXATAS (MATEMÁTICA E FÍSICA)
# ============================================================

def agente_modo_exatas(consulta, categoria):
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"

    print(f"[AGENTE EXATAS] Recebida consulta: {consulta}")

    prompt_sistema_exatas = f"""
    Você é Sacy, um assistente de IA com o papel de um Professor de Exatas (Matemática e Física) 
    especializado em ENEM e vestibulares.
    Sua tarefa é responder a consulta do aluno de forma didática, passo a passo, em MARKDOWN.

    **Instruções de Formatação (OBRIGATÓRIO USAR MARKDOWN):**
    1.  **Título Principal:** Use `###` para o conceito principal.
    2.  **Definição:** Explique de forma direta e simples.
    3.  **Fórmula:** Mostre em formato claro, ex: `ax² + bx + c = 0`.
    4.  **Passo a Passo:** Use `#### Como aplicar?` e uma lista ordenada.
    5.  **Exemplo Prático:** Mostre um exemplo resolvido.
    6.  **Importância no ENEM:** Destaque como o tema aparece na prova.
    """

    try:
        prompt_combinado = f"{prompt_sistema_exatas}\n\n---\nCONSULTA DO ALUNO:\n{consulta}\n---"
        response = model_agent.generate_content(prompt_combinado)
        resposta_html = markdown(response.text)

        return f"""
        <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #818cf8;
        border-radius:15px;padding:20px;background-color:#1e1b4b;'>
            <h2 style='color:#c7d2fe;display:flex;align-items:center;gap:8px;'>
                <img src='https://placehold.co/30x30/c7d2fe/1e1b4b?text=CALC' width='30' height='30'>
                Modo Foco ENEM: {categoria.title()}
            </h2>
            <div style='font-size:15px;line-height:1.7;color:#d1d5db;text-align:justify;margin-top:15px;'>
                {resposta_html}
            </div>
        </div>
        """
    except Exception as e:
        print(f"❌ Erro no agente_modo_exatas: {e}")
        return f"<p>Ocorreu um erro ao gerar a resposta de Exatas: {e}</p>"


# ============================================================
# 🎨 AGENTE 2: ARTE (PLACEHOLDER)
# ============================================================

def agente_modo_arte_placeholder(consulta):
    print(f"[AGENTE ARTE] Placeholder ativado para: {consulta}")
    api_url = f"https://api.artic.edu/api/v1/artworks/search?q={consulta.replace(' ', '+')}&limit=1"

    return f"""
    <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #f0abfc;
    border-radius:15px;padding:20px;background-color:#2e1b4b;'>
        <h2 style='color:#f5d0fe;display:flex;align-items:center;gap:8px;'>
            <img src='https://placehold.co/30x30/f5d0fe/2e1b4b?text=ART' width='30' height='30'>
            Modo Foco ENEM: Arte (Em Breve)
        </h2>
        <p><strong>[PLACEHOLDER]</strong> O agente especializado em Arte será ativado futuramente.</p>
        <p>Consulta simulada: <strong>{consulta}</strong></p>
        <p><em>API que será usada: <code>{api_url}</code></em></p>
    </div>
    """


# ============================================================
# 📚 AGENTE 3: LITERATURA (PLACEHOLDER)
# ============================================================

def agente_modo_literatura_placeholder(consulta):
    print(f"[AGENTE LITERATURA] Placeholder ativado para: {consulta}")
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={consulta.replace(' ', '+')}"
    return f"""
    <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #67e8f9;
    border-radius:15px;padding:20px;background-color:#1b4b4b;'>
        <h2 style='color:#a5f3fc;display:flex;align-items:center;gap:8px;'>
            <img src='https://placehold.co/30x30/a5f3fc/1b4b4b?text=LIT' width='30' height='30'>
            Modo Foco ENEM: Literatura (Em Breve)
        </h2>
        <p><strong>[PLACEHOLDER]</strong> O agente especializado em Literatura será ativado futuramente.</p>
        <p>Consulta: <strong>{consulta}</strong></p>
        <p><em>API que será usada: <code>{api_url}</code></em></p>
    </div>
    """


# ============================================================
# ⚗️ AGENTE 4: QUÍMICA (PLACEHOLDER)
# ============================================================

def agente_modo_quimica_placeholder(consulta):
    print(f"[AGENTE QUIMICA] Placeholder ativado para: {consulta}")
    return f"""
    <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #86efac;
    border-radius:15px;padding:20px;background-color:#1b4b2e;'>
        <h2 style='color:#bbf7d0;display:flex;align-items:center;gap:8px;'>
            <img src='https://placehold.co/30x30/bbf7d0/1b4b2e?text=Q' width='30' height='30'>
            Modo Foco ENEM: Química (Em Breve)
        </h2>
        <p><strong>[PLACEHOLDER]</strong> O agente especializado em Química será ativado futuramente.</p>
        <p>Consulta: <strong>{consulta}</strong></p>
    </div>
    """


# ============================================================
# 🌍 AGENTE 5: GEOGRAFIA (PLACEHOLDER)
# ============================================================

def agente_modo_geografia_placeholder(consulta):
    print(f"[AGENTE GEOGRAFIA] Placeholder ativado para: {consulta}")
    api_url = f"https://restcountries.com/v3.1/name/{consulta.replace(' ', '+')}"
    return f"""
    <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #fde047;
    border-radius:15px;padding:20px;background-color:#4b441b;'>
        <h2 style='color:#fef08a;display:flex;align-items:center;gap:8px;'>
            <img src='https://placehold.co/30x30/fef08a/4b441b?text=GEO' width='30' height='30'>
            Modo Foco ENEM: Geografia (Em Breve)
        </h2>
        <p><strong>[PLACEHOLDER]</strong> O agente especializado em Geografia será ativado futuramente.</p>
        <p><em>URL da API que será usada: <code>{api_url}</code></em></p>
    </div>
    """


# ============================================================
# ✍️ AGENTE 6: REDAÇÃO (PLACEHOLDER + IMPLEMENTADO)
# ============================================================

def agente_modo_redacao_placeholder(consulta):
    print(f"[AGENTE REDAÇÃO] Placeholder ativado.")
    return f"""
    <div style='font-family:Inter, sans-serif;color:#f1f1f1;border:1px solid #fda4af;
    border-radius:15px;padding:20px;background-color:#4b1b24;'>
        <h2 style='color:#fecdd3;display:flex;align-items:center;gap:8px;'>
            <img src='https://placehold.co/30x30/fecdd3/4b1b24?text=R' width='30' height='30'>
            Modo Foco ENEM: Redação (Em Breve)
        </h2>
        <p><strong>[PLACEHOLDER]</strong> O agente de Redação será ativado futuramente.</p>
    </div>
    """


def agente_modo_redacao(consulta):
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"
    print(f"[AGENTE REDAÇÃO] Recebida consulta para análise...")

    prompt_sistema_redacao = """
    Você é Sacy, um corretor de Redação do ENEM. Analise o texto do aluno de forma didática.
    Use as 5 competências do ENEM e responda em Markdown.
    """

    try:
        prompt = f"{prompt_sistema_redacao}\n\n---\nREDAÇÃO DO ALUNO:\n{consulta}\n---"
        response = model_agent.generate_content(prompt)
        resposta_html = markdown(response.text)

        return f"""
        <div style='font-family:Inter,sans-serif;color:#f1f1f1;border:1px solid #fda4af;
        border-radius:15px;padding:20px;background-color:#4b1b24;'>
            <h2 style='color:#fecdd3;display:flex;align-items:center;gap:8px;'>
                <img src='https://placehold.co/30x30/fecdd3/4b1b24?text=R' width='30' height='30'>
                Modo Foco ENEM: Redação
            </h2>
            {resposta_html}
        </div>
        """
    except Exception as e:
        print(f"❌ Erro no agente_modo_redacao: {e}")
        return f"<p>Erro ao gerar resposta de Redação: {e}</p>"


# ============================================================
# 📚 AGENTE 7: LITERATURA (IMPLEMENTADO)
# ============================================================

def agente_modo_literatura(consulta):
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"
    print(f"[AGENTE LITERATURA] Consulta recebida: {consulta}")

    prompt = f"""
    Você é Sacy, um professor de LITERATURA do ENEM.
    Explique o tema solicitado com contexto histórico, autores e relevância.
    Use Markdown.

    ### Estrutura:
    - `### Título`
    - `#### Contexto histórico e escola`
    - `#### Características`
    - `#### Autores e obras`
    - `#### Relevância no ENEM`

    Tema: {consulta}
    """
    try:
        response = model_agent.generate_content(prompt)
        resposta_html = markdown(response.text)

        return f"""
        <div style='font-family:Inter,sans-serif;color:#f1f1f1;border:1px solid #67e8f9;
        border-radius:15px;padding:20px;background-color:#1b4b4b;'>
            <h2 style='color:#a5f3fc;display:flex;align-items:center;gap:8px;'>
                <img src='https://placehold.co/30x30/a5f3fc/1b4b4b?text=LIT' width='30' height='30'>
                Modo Foco ENEM: Literatura
            </h2>
            {resposta_html}
        </div>
        """
    except Exception as e:
        print(f"❌ Erro no agente_modo_literatura: {e}")
        return f"<p>Erro ao gerar resposta de Literatura: {e}</p>"


# ============================================================
# ⚗️ AGENTE 8: QUÍMICA (IMPLEMENTADO)
# ============================================================

def agente_modo_quimica(consulta):
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"
    print(f"[AGENTE QUIMICA] Consulta recebida: {consulta}")

    prompt = f"""
    Você é Sacy, um professor de QUÍMICA do ENEM.
    Explique o tema solicitado de forma clara e aplicada.
    Mostre exemplos e contextualize.

    ### Estrutura:
    - `### Conceito`
    - `#### Fórmulas e explicações`
    - `#### Exemplo prático`
    - `#### Importância no ENEM`

    Tema: {consulta}
    """
    try:
        response = model_agent.generate_content(prompt)
        resposta_html = markdown(response.text)

        return f"""
        <div style='font-family:Inter,sans-serif;color:#f1f1f1;border:1px solid #86efac;
        border-radius:15px;padding:20px;background-color:#1b4b2e;'>
            <h2 style='color:#bbf7d0;display:flex;align-items:center;gap:8px;'>
                <img src='https://placehold.co/30x30/bbf7d0/1b4b2e?text=Q' width='30' height='30'>
                Modo Foco ENEM: Química
            </h2>
            {resposta_html}
        </div>
        """
    except Exception as e:
        print(f"❌ Erro no agente_modo_quimica: {e}")
        return f"<p>Erro ao gerar resposta de Química: {e}</p>"


# ============================================================
# 🌎 AGENTE 9: GEOGRAFIA (IMPLEMENTADO)
# ============================================================

def agente_modo_geografia(consulta):
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"
    print(f"[AGENTE GEOGRAFIA] Consulta recebida: {consulta}")

    prompt = f"""
    Você é Sacy, um professor de GEOGRAFIA do ENEM.
    Explique o tema solicitado com foco em teoria, atualidades e contexto global.
    Use Markdown.

    ### Estrutura:
    - `### Título`
    - `#### Conceitos principais`
    - `#### Exemplos e dados`
    - `#### Atualidades e conexões`
    - `#### Relevância no ENEM`

    Tema: {consulta}
    """
    try:
        response = model_agent.generate_content(prompt)
        resposta_html = markdown(response.text)

        return f"""
        <div style='font-family:Inter,sans-serif;color:#f1f1f1;border:1px solid #fde047;
        border-radius:15px;padding:20px;background-color:#4b441b;'>
            <h2 style='color:#fef08a;display:flex;align-items:center;gap:8px;'>
                <img src='https://placehold.co/30x30/fef08a/4b441b?text=GEO' width='30' height='30'>
                Modo Foco ENEM: Geografia
            </h2>
            {resposta_html}
        </div>
        """
    except Exception as e:
        print(f"❌ Erro no agente_modo_geografia: {e}")
        return f"<p>Erro ao gerar resposta de Geografia: {e}</p>"
