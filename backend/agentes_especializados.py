import os
import json
import google.generativeai as genai
from markdown import markdown

# --- Configuração do Cliente Gemini ---
# (Esta API Key é usada internamente pelos agentes, não pelo servidor)
try:
    API_KEY = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4" # Deixe em branco
    if not API_KEY:
        API_KEY = os.environ.get("GEMINI_API_KEY")

    genai.configure(api_key=API_KEY)
    # Modelo para geração de conteúdo (os agentes)
    model_agent = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    print("🤖 Cliente Gemini (Agentes) configurado com sucesso.")
except Exception as e:
    print(f"❌ ERRO GRAVE: Falha ao configurar o cliente Gemini (Agentes). Erro: {e}")
    model_agent = None

# --- Agente 1: Modo Exatas (Matemática/Física) ---

def agente_modo_exatas(consulta, categoria):
    """
    Agente especializado em responder perguntas de Matemática e Física
    como um professor.
    """
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"

    print(f"[AGENTE EXATAS] Recebida consulta: {consulta}")

    # --- INÍCIO DA CORREÇÃO (PROMPT) ---
    # Este é o "cérebro" do professor de exatas
    # Alterado para pedir MARKDOWN, não HTML
    prompt_sistema_exatas = f"""
    Você é Sacy, um assistente de IA com o papel de um Professor de Exatas (Matemática e Física) 
    especializado em ENEM e vestibulares.
    Sua tarefa é responder a consulta do aluno de forma didática, passo a passo, em MARKDOWN.

    **Instruções de Formatação (OBRIGATÓRIO USAR MARKDOWN):**
    1.  **Título Principal:** Use `###` para o conceito principal (ex: `### O que é a Fórmula de Bhaskara?`).
    2.  **Definição:** Use parágrafos normais.
    3.  **Fórmula (se houver):** Apresente a fórmula claramente usando backticks (ex: `ax² + bx + c = 0`).
    4.  **Passo a Passo:** Use `#### Como aplicar?` seguido de uma lista ordenada (ex: `1. ...`, `2. ...`).
    5.  **Exemplo Prático:** Use `#### Exemplo Prático`.
    6.  **Importância no ENEM:** Use `#### Importância no ENEM`.
    7.  **NÃO USE TAGS HTML**. Use apenas formatação Markdown.
    """
    # --- FIM DA CORREÇÃO (PROMPT) ---

    try:
        # Combinamos o "sistema" (as instruções) e o "usuário" (a consulta)
        prompt_combinado = f"""
        {prompt_sistema_exatas}

        ---
        CONSULTA DO ALUNO:
        {consulta}
        ---
        """
        
        # --- INÍCIO DA CORREÇÃO (CHAMADA API) ---
        # Removemos o 'generation_config' que estava a causar o erro 400.
        # O modelo agora devolverá text/plain (Markdown) por defeito.
        response = model_agent.generate_content(prompt_combinado)
        
        # Convertemos a resposta (Markdown) para HTML
        resposta_html = markdown(response.text)
        # --- FIM DA CORREÇÃO (CHAMADA API) ---
        
        # Adiciona um wrapper para garantir o estilo do frontend
        return f"""
        <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #818cf8; border-radius:15px; padding:20px; background-color:#1e1b4b;'>
            <h2 style='color:#c7d2fe; display:flex; align-items:center; gap:8px;'>
                <img src='https://placehold.co/30x30/c7d2fe/1e1b4b?text=CALC' width='30' height='30' alt='Modo Exatas' style='border-radius: 4px;'>
                Modo Foco ENEM: {categoria.title()}
            </h2>
            <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
                {resposta_html}
            </div>
        </div>
        """

    except Exception as e:
        print(f"❌ Erro no agente_modo_exatas: {e}")
        return f"<p>Ocorreu um erro ao gerar a resposta de Exatas: {e}</p>"


# --- Agente 2: Modo Arte (Placeholder) ---

def agente_modo_arte_placeholder(consulta):
    """
    Placeholder para o Agente de Arte (Upgrade 9).
    Quando implementado, chamará a API do Art Institute of Chicago.
    """
    print(f"[AGENTE ARTE] Placeholder ativado para: {consulta}")
    
    # Simula a busca pela API
    api_url = f"https://api.artic.edu/api/v1/artworks/search?q={consulta.replace(' ', '+')}&limit=1"
    
    resposta_html = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #f0abfc; border-radius:15px; padding:20px; background-color:#2e1b4b;'>
        <h2 style='color:#f5d0fe; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/f5d0fe/2e1b4b?text=ART' width='30' height='30' alt='Modo Arte' style='border-radius: 4px;'>
            Modo Foco ENEM: Arte (Em Breve)
        </h2>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
            <p><strong>[PLACEHOLDER]</strong> O agente especializado em Arte (Upgrade 9) será ativado para esta consulta.</p>
            <p>Quando implementado, ele buscará por "<strong>{consulta}</strong>" diretamente na API do <strong>Art Institute of Chicago</strong> e em outras APIs de museus para trazer informações sobre obras, artistas e movimentos artísticos relevantes para o ENEM.</p>
            <p><em>URL da API que será usada: <code>{api_url}</code></em></p>
        </div>
    </div>
    """
    return resposta_html

# --- Agente 3: Modo Literatura (Placeholder) ---

def agente_modo_literatura_placeholder(consulta):
    """
    Placeholder para o Agente de Literatura (Upgrade 10).
    Quando implementado, chamará a API do Google Books.
    """
    print(f"[AGENTE LITERATURA] Placeholder ativado para: {consulta}")
    
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={consulta.replace(' ', '+')}"
    
    resposta_html = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #67e8f9; border-radius:15px; padding:20px; background-color:#1b4b4b;'>
        <h2 style='color:#a5f3fc; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/a5f3fc/1b4b4b?text=LIT' width='30' height='30' alt='Modo Literatura' style='border-radius: 4px;'>
            Modo Foco ENEM: Literatura (Em Breve)
        </h2>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
            <p><strong>[PLACEHOLDER]</strong> O agente especializado em Literatura (Upgrade 10) será ativado para esta consulta.</p>
            <p>Quando implementado, ele buscará por "<strong>{consulta}</strong>" diretamente na <strong>API do Google Books</strong> para trazer resumos de obras, biografias de autores e análise de escolas literárias do ENEM.</p>
            <p><em>URL da API que será usada: <code>{api_url}</code></em></p>
        </div>
    </div>
    """
    return resposta_html

# --- Agente 4: Modo Química (Placeholder) ---

def agente_modo_quimica_placeholder(consulta):
    """
    Placeholder para o Agente de Química (Upgrade 5).
    Quando implementado, chamará a API 'Elements'.
    """
    print(f"[AGENTE QUIMICA] Placeholder ativado para: {consulta}")
    
    api_url = "https://api.api-ninjas.com/v1/elements?name=..."
    
    resposta_html = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #86efac; border-radius:15px; padding:20px; background-color:#1b4b2e;'>
        <h2 style='color:#bbf7d0; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/bbf7d0/1b4b2e?text=Q' width='30' height='30' alt='Modo Química' style='border-radius: 4px;'>
            Modo Foco ENEM: Química (Em Breve)
        </h2>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
            <p><strong>[PLACEHOLDER]</strong> O agente especializado em Química (Upgrade 5) será ativado para esta consulta.</p>
            <p>Quando implementado, ele usará a <strong>API 'Periodic Table Elements'</strong> para buscar dados técnicos sobre elementos (massa atômica, distribuição eletrônica, etc.) e explicará como eles se relacionam com estequiometria e reações no ENEM.</p>
            <p><em>API que será usada: <code>{api_url}</code></em></p>
        </div>
    </div>
    """
    return resposta_html

# --- Agente 5: Modo Geografia (Placeholder) ---

def agente_modo_geografia_placeholder(consulta):
    """
    Placeholder para o Agente de Geografia (Upgrade 7).
    Quando implementado, chamará a API 'REST Countries'.
    """
    print(f"[AGENTE GEOGRAFIA] Placeholder ativado para: {consulta}")
    
    api_url = f"https://restcountries.com/v3.1/name/{consulta.replace(' ', '+')}"
    
    resposta_html = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #fde047; border-radius:15px; padding:20px; background-color:#4b441b;'>
        <h2 style='color:#fef08a; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/fef08a/4b441b?text=GEO' width='30' height='30' alt='Modo Geografia' style='border-radius: 4px;'>
            Modo Foco ENEM: Geografia (Em Breve)
        </h2>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
            <p><strong>[PLACEHOLDER]</strong> O agente especializado em Geografia (Upgrade 7) será ativado para esta consulta.</p>
            <p>Quando implementado, ele usará a <strong>API 'REST Countries'</strong> para buscar dados sobre "<strong>{consulta}</strong>" (população, PIB, clima, fronteiras) e conectará esses dados a temas de geopolítica e geografia física do ENEM.</p>
            <p><em>URL da API que será usada: <code>{api_url}</code></em></p>
        </div>
    </div>
    """
    return resposta_html

# --- Agente 6: Modo Redação (Placeholder) ---

def agente_modo_redacao_placeholder(consulta):
    """
    Placeholder para o Agente de Redação (Upgrade 8).
    Quando implementado, usará uma IA (Gemini ou outra) para análise.
    """
    print(f"[AGENTE REDAÇÃO] Placeholder ativado.")
    
    resposta_html = f"""
    <div style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #fda4af; border-radius:15px; padding:20px; background-color:#4b1b24;'>
        <h2 style='color:#fecdd3; display:flex; align-items:center; gap:8px;'>
            <img src='https://placehold.co/30x30/fecdd3/4b1b24?text=R' width='30' height='30' alt='Modo Redação' style='border-radius: 4px;'>
            Modo Foco ENEM: Redação (Em Breve)
        </h2>
        <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
            <p><strong>[PLACEHOLDER]</strong> O agente especializado em Redação (Upgrade 8) será ativado.</p>
            <p>Quando implementado, este agente usará uma IA avançada (como o Gemini ou outra API de texto longa) para analisar a sua redação colada, verificar a estrutura (introdução, desenvolvimento, conclusão) e dar sugestões com base nas 5 competências do ENEM.</p>
        </div>
    </div>
    """
    return resposta_html

# --- Agente 6: Modo Redação (IMPLEMENTADO) ---

def agente_modo_redacao(consulta):
    """
    Agente especializado em analisar redações (Upgrade 8).
    Usa o Gemini como um corretor do ENEM.
    """
    if not model_agent:
        return "<p>Erro: O modelo de IA para agentes não foi inicializado.</p>"

    print(f"[AGENTE REDAÇÃO] Recebida consulta para análise...")

    # Este é o "cérebro" do corretor do ENEM
    prompt_sistema_redacao = f"""
    Você é Sacy, um assistente de IA com o papel de um Corretor de Redação do ENEM.
    Sua tarefa é analisar a redação do aluno, focando nas 5 Competências do ENEM.
    Responda em MARKDOWN.

    **Instruções de Análise (OBRIGATÓRIO):**
    1.  **Título:** Use `### Análise da Redação (Modo Foco ENEM)`.
    2.  **Análise por Competência:** Crie um subtítulo `#### Análise por Competência` e uma lista:
        * `**Competência 1 (Domínio da norma culta):**` (Sua análise sobre gramática, ortografia).
        * `**Competência 2 (Compreensão do tema e estrutura):**` (Sua análise se o aluno fugiu do tema e usou a estrutura dissertativa-argumentativa).
        * `**Competência 3 (Seleção de argumentos):**` (Sua análise sobre a qualidade dos argumentos e repertório).
        * `**Competência 4 (Coesão e coerência):**` (Sua análise sobre o uso de conectivos e a fluidez do texto).
        * `**Competência 5 (Proposta de intervenção):**` (Sua análise se a proposta de intervenção está completa - agente, ação, modo, efeito, detalhamento).
    3.  **Feedback Geral:** Crie um subtítulo `#### Feedback Geral` com:
        * `**Pontos Fortes:**` (Uma lista `*` do que o aluno fez bem).
        * `**Pontos a Melhorar:**` (Uma lista `*` do que o aluno precisa focar).
    4.  **Nota Provisória:** Crie um subtítulo `#### Nota Provisória` e dê uma nota estimada de 0 a 1000.
    5.  **NÃO USE TAGS HTML**. Use apenas formatação Markdown.
    """

    try:
        # Combinamos o "sistema" (as instruções) e o "usuário" (a redação)
        prompt_combinado = f"""
        {prompt_sistema_redacao}

        ---
        REDAÇÃO DO ALUNO PARA ANÁLISE:
        {consulta}
        ---
        """
        
        response = model_agent.generate_content(prompt_combinado)
        
        # Convertemos a resposta (Markdown) para HTML
        resposta_html = markdown(response.text)
        
        # Adiciona um wrapper para garantir o estilo do frontend
        return f"""
        <style>
            .modo-enem-redacao h3 {{
                color: #fecdd3;
                font-size: 1.25rem;
                border-bottom: 1px solid #db2777;
                padding-bottom: 8px;
                margin-top: 1.5rem;
                margin-bottom: 1rem;
            }}
            .modo-enem-redacao h4 {{
                color: #fda4af;
                font-size: 1.125rem;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }}
            .modo-enem-redacao p {{
                margin-bottom: 1rem;
            }}
            .modo-enem-redacao ul {{
                list-style-type: disc;
                margin-left: 1.5rem;
                margin-bottom: 1rem;
            }}
            .modo-enem-redacao li {{
                padding-left: 0.5rem;
                margin-bottom: 0.5rem;
            }}
            .modo-enem-redacao strong {{
                color: #fbcfe8; /* Rosa mais claro */
            }}
        </style>

        <div class='modo-enem-redacao' style='font-family:Inter, sans-serif; color:#f1f1f1; border: 1px solid #fda4af; border-radius:15px; padding:20px; background-color:#4b1b24;'>
            <h2 style='color:#fecdd3; display:flex; align-items:center; gap:8px; margin-top:0;'>
                <img src='https://placehold.co/30x30/fecdd3/4b1b24?text=R' width='30' height='30' alt='Modo Redação' style='border-radius: 4px;'>
                Modo Foco ENEM: Redação
            </h2>
            <div style='font-size:15px; line-height:1.7; color:#d1d5db; text-align:justify; margin-top: 15px;'>
                {resposta_html}
            </div>
        </div>
        """

    except Exception as e:
        print(f"❌ Erro no agente_modo_redacao: {e}")
        return f"<p>Ocorreu um erro ao gerar a resposta de Redação: {e}</p>"

