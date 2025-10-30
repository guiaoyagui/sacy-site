#!/usr/bin/env python3
"""
Servidor API Flask para integração com o sistema multi-agente
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from agent_geral import AgentGeral

app = Flask(__name__)
CORS(app)  # Permitir CORS para desenvolvimento

# Instanciar o Agent Geral
agent_geral = AgentGeral()

@app.route('/')
def home():
    """Página inicial com documentação da API"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Sistema Multi-Agente NASA</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #1e3a8a; }
            .endpoint { background: #f8fafc; padding: 15px; margin: 15px 0; border-left: 4px solid #3b82f6; }
            .method { background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
            pre { background: #1f2937; color: #f9fafb; padding: 15px; border-radius: 4px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 API Sistema Multi-Agente NASA</h1>
            <p>API para coordenação de agentes especializados em análise de dados espaciais, pesquisa científica e planejamento de missões.</p>
            
            <h2>Endpoints Disponíveis</h2>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> /api/processar-consulta</h3>
                <p>Processa uma consulta através do sistema multi-agente.</p>
                <h4>Corpo da Requisição:</h4>
                <pre>{
  "consulta": "Quero analisar dados de missões da NASA"
}</pre>
                <h4>Resposta:</h4>
                <pre>Painel dinâmico em formato Markdown com resultados dos agentes</pre>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> /api/status</h3>
                <p>Verifica o status da API e dos agentes disponíveis.</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> /api/agentes</h3>
                <p>Lista todos os agentes especializados disponíveis.</p>
            </div>
            
            <h2>Agentes Especializados</h2>
            <ul>
                <li><strong>Agent CSV (Data Analyst):</strong> Processamento de arquivos CSV da NASA, análise estatística e visualizações</li>
                <li><strong>Agent Literatura (Research Analyst):</strong> Mineração de textos científicos e identificação de lacunas de conhecimento</li>
                <li><strong>Agent Missões (Mission Planner):</strong> Insights para planejamento de missões e análise de riscos</li>
            </ul>
            
            <h2>Fontes de Dados</h2>
            <ul>
                <li><a href="https://public.ksc.nasa.gov/nslsl" target="_blank">NSLSL - NASA Space Life Sciences Library</a></li>
                <li><a href="https://science.nasa.gov/biological-physical/data" target="_blank">OSDR - Open Science Data Repository</a></li>
                <li><a href="https://github.com/jgalazka/SB_publications/tree/main" target="_blank">GitHub SB_publications</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/processar-consulta', methods=['POST'])
def processar_consulta():
    """Endpoint principal para processar consultas do usuário"""
    try:
        data = request.get_json()
        
        if not data or 'consulta' not in data:
            return jsonify({'erro': 'Consulta não fornecida'}), 400
        
        consulta_texto = data['consulta'].strip()
        
        if not consulta_texto:
            return jsonify({'erro': 'Consulta vazia'}), 400
        
        # Processar consulta através do Agent Geral
        resultado = agent_geral.processar_consulta(consulta_texto)
        
        return resultado, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        print(f"Erro ao processar consulta: {e}")
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Endpoint para verificar o status da API"""
    return jsonify({
        'status': 'online',
        'versao': '1.0.0',
        'agentes_disponiveis': len(agent_geral.agentes_disponiveis),
        'historico_consultas': len(agent_geral.historico_consultas)
    })

@app.route('/api/agentes', methods=['GET'])
def listar_agentes():
    """Endpoint para listar agentes disponíveis"""
    agentes_info = []
    
    for agente_tipo, descricao in agent_geral.agentes_disponiveis.items():
        agentes_info.append({
            'tipo': agente_tipo.value,
            'nome': descricao,
            'status': 'ativo'
        })
    
    return jsonify({
        'agentes': agentes_info,
        'total': len(agentes_info)
    })

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    """Endpoint para obter histórico de consultas"""
    historico = []
    
    for consulta in agent_geral.historico_consultas[-10:]:  # Últimas 10 consultas
        historico.append({
            'id': consulta.id_consulta,
            'texto': consulta.texto,
            'timestamp': consulta.timestamp
        })
    
    return jsonify({
        'historico': historico,
        'total': len(agent_geral.historico_consultas)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor API do Sistema Multi-Agente NASA...")
    print("📡 Agentes disponíveis:")
    for agente_tipo, descricao in agent_geral.agentes_disponiveis.items():
        print(f"   - {descricao}")
    print("\n🌐 Servidor rodando em: http://localhost:5000")
    print("📚 Documentação da API: http://localhost:5000")
    print("🔗 Interface React: http://localhost:3000 (se estiver rodando)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
