#!/usr/bin/env python3
"""
Agent Geral (Search Master)
Coordenador e interface principal do sistema multi-agente
"""

import datetime
import os
import base64
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI

from agent_csv import AgentCSV
from agent_literatura import AgentLiteratura
from agent_missoes import AgentMissoes

# Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AgentType(Enum):
    CSV = "csv"
    LITERATURA = "literatura"
    MISSOES = "missoes"

@dataclass
class ConsultaUsuario:
    texto: str
    timestamp: str
    id_consulta: str

@dataclass
class ResultadoAgente:
    agente_tipo: AgentType
    dados: Dict[str, Any]
    sucesso: bool
    mensagem: str

class AgentGeral:
    def __init__(self):
        self.historico_consultas: List[ConsultaUsuario] = []
        self.agentes_disponiveis = {
            AgentType.CSV: "Agent Especialista em CSV (Data Analyst)",
            AgentType.LITERATURA: "Agent Especialista em Literatura (Research Analyst)",
            AgentType.MISSOES: "Agent Especialista em Missões (Mission Planner)"
        }
        self.agent_csv = AgentCSV()
        self.agent_literatura = AgentLiteratura()
        self.agent_missoes = AgentMissoes()

        # Pasta para salvar imagens geradas
        self.imagem_dir = os.path.join(os.path.dirname(__file__), "generated_images")
        os.makedirs(self.imagem_dir, exist_ok=True)

    def analisar_intencao(self, consulta: str) -> List[AgentType]:
        consulta_lower = consulta.lower()
        agentes_necessarios = []
        
        # Palavras-chave para acionar agentes específicos
        if any(palavra in consulta_lower for palavra in ['dados', 'csv', 'análise', 'gráfico']):
            agentes_necessarios.append(AgentType.CSV)
        if any(palavra in consulta_lower for palavra in ['artigo', 'pesquisa', 'literatura', 'estudo', 'o que é', 'como']):
            agentes_necessarios.append(AgentType.LITERATURA)
        if any(palavra in consulta_lower for palavra in ['missão', 'planejamento', 'risco', 'espacial', 'nasa']):
            agentes_necessarios.append(AgentType.MISSOES)
        
        if not agentes_necessarios:
            return list(AgentType)
        return agentes_necessarios

    def gerar_imagem(self, prompt: str) -> str | None:
        """
        Gera uma imagem relacionada ao tema da consulta.
        Retorna o caminho local da imagem.
        """
        try:
            print(f"🎨 Gerando imagem para o tema: {prompt}")
            response = client.images.generate(
                model="gpt-image-1",
                prompt=f"Ilustração realista e moderna sobre {prompt}, estilo científico e visual limpo.",
                size="1024x1024"
            )

            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            filename = f"image_{datetime.datetime.now().timestamp()}.png"
            filepath = os.path.join(self.imagem_dir, filename)

            with open(filepath, "wb") as f:
                f.write(image_bytes)

            print(f"🖼️ Imagem salva em: {filepath}")
            return filepath
        except Exception as e:
            print(f"⚠️ Erro ao gerar imagem: {e}")
            return None

    def sintetizar_resultados(self, resultados: List[ResultadoAgente]) -> Dict[str, Any]:
        sintese = {"resumo_executivo": "Análise concluída.", "resultados_por_agente": {}}
        for resultado in resultados:
            sintese["resultados_por_agente"][resultado.agente_tipo.value] = {
                "dados": resultado.dados,
                "status": "sucesso" if resultado.sucesso else "erro",
                "mensagem": resultado.mensagem
            }
        return sintese

    def gerar_painel_dinamico(self, sintese: Dict[str, Any], imagem: str | None, consulta: str) -> str:
        painel = f'# 🚀 Resultado da Análise: **{consulta}**\n\n'

        # Se houver imagem gerada, adiciona no topo
        if imagem:
            nome_arquivo = os.path.basename(imagem)
            painel += f"![Imagem gerada sobre {consulta}](generated_images/{nome_arquivo})\n\n"

        resultado_literatura = sintese["resultados_por_agente"].get("literatura")

        if resultado_literatura and resultado_literatura["status"] == "sucesso":
            resumo = resultado_literatura["dados"].get("resumo_gerado", "Não foi possível gerar um resumo.")
            painel += f'## 🧠 Análise da Literatura\n{resumo}\n'
        else:
            painel += "❌ Não foi possível obter uma resposta do agente de literatura.\n"

        painel += "\n---\n🕒 *Gerado automaticamente pelo Search Master Agent*"
        return painel

    def processar_consulta(self, texto_consulta: str) -> Dict[str, Any]:
        consulta = ConsultaUsuario(
            texto=texto_consulta,
            timestamp=datetime.datetime.now().isoformat(),
            id_consulta=f"consulta_{len(self.historico_consultas) + 1}"
        )
        self.historico_consultas.append(consulta)
        
        agentes_a_acionar = self.analisar_intencao(consulta.texto)
        resultados_agentes = []
        
        for agente_tipo in agentes_a_acionar:
            try:
                if agente_tipo == AgentType.LITERATURA:
                    print(f"📘 Agent Geral: Acionando Agent Literatura com consulta: {consulta.texto}")
                    lit_result = self.agent_literatura.processar_consulta_literatura(consulta.texto)
                    resultados_agentes.append(ResultadoAgente(AgentType.LITERATURA, lit_result, True, "Pesquisa de literatura concluída."))
            except Exception as e:
                print(f"Erro ao executar Agent {agente_tipo.value}: {e}")
                resultados_agentes.append(ResultadoAgente(agente_tipo, {}, False, str(e)))

        # Gera imagem do tema
        imagem_path = self.gerar_imagem(texto_consulta)

        # Monta resultado final
        sintese = self.sintetizar_resultados(resultados_agentes)
        painel = self.gerar_painel_dinamico(sintese, imagem_path, texto_consulta)

        return {
            "painel": painel,
            "imagem": imagem_path
        }
