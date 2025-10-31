Assistente de Pesquisa "Sacy" (Nome Provisório)

Este é um projeto full-stack que funciona como um assistente de pesquisa inteligente, desenhado para transformar a sobrecarga de informação da web em conhecimento acionável. A aplicação permite ao utilizador pesquisar um tópico, receber um resumo formatado e, em seguida, interagir com esse resumo usando IA generativa para simplificar o conteúdo ou criar um quiz interativo.



✨ Funcionalidades

Pesquisa e Resumo Inteligente: O utilizador insere um tópico (ex: "Marte") e o backend Python pesquisa na web, faz scraping do conteúdo e devolve um resumo completo formatado em HTML, incluindo imagens e links.
Limpeza de HTML no Frontend: Uma função cleanHtmlResult no React interceta o HTML do backend e remove à força estilos problemáticos (como background-color: #ffffff), garantindo a consistência visual no modo escuro.
Simplificação com IA (Gemini): Um botão "Simplificar Resumo" envia o resumo para a API Gemini e pede uma versão mais simples, formatada em HTML com emojis e tópicos, ideal para iniciantes.
Quiz Interativo (Gemini): Um botão "Gerar Quiz" envia o resumo para a API Gemini e pede um quiz de escolha múltipla (em formato JSON). O frontend constrói um formulário interativo onde o utilizador pode responder e ser corrigido.

🚀 Arquitetura do Projeto

Este projeto tem uma arquitetura híbrida interessante que divide as tarefas:
Fluxo 1: Backend Local (Python/Flask)
Usado para a pesquisa principal, que exige scraping da web (uma tarefa que não pode ser feita no browser).
Fluxo: React -> Flask -> AgentLiteratura -> Web (Scraping) -> Flask -> React.
Fluxo 2: API Externa (Gemini)
Usado para tarefas de IA pura (simplificação e geração de quiz), que podem ser feitas diretamente no browser.
Fluxo: React -> API Gemini (JSON/HTML) -> React.

graph TD
    subgraph Frontend (Browser)
        A[Utilizador] --> B{Dashboard (React)};
        B --"1. Pesquisa Principal"--> C[Backend: Flask];
        B --"2. Funções Extra (Quiz/Simplificar)"--> G[API Gemini];
        G --> B;
    end

    subgraph Backend (Localhost:5000)
        C --"3. Chama Agente"--> E[agent_literatura.py];
        E --"4. Pesquisa e faz Scraping"--> F[(Web / Wikipedia)];
        F --> E;
        E --"5. Cria Resumo em HTML"--> C;
    end
    
    C --"6. Devolve JSON com HTML"--> B;


🛠️ Tecnologias Utilizadas

Frontend:
React / Next.js
Tailwind CSS (para estilização)
TypeScript
Backend:
Python
Flask (como servidor API)
Flask-CORS (para permitir a comunicação entre localhost:3000 e localhost:5000)
(Bibliotecas do agent_literatura como requests, beautifulsoup4, etc.)

APIs:
API Google Gemini (para simplificação e geração de quiz)
