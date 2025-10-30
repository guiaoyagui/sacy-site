#!/usr/bin/env python3
"""
Agent Especialista em Missões (Mission Planner)
Insights acionáveis para planejamento
"""

import json
from typing import Dict, Any, List, Optional

class AgentMissoes:
    """
    Agent Especialista em Missões - Insights acionáveis para planejamento
    
    Responsabilidades:
    - Análise de riscos e oportunidades
    - Recomendações para investimentos
    - Identificação de tecnologias promissoras
    - Planejamento de missões lunares/marcianas
    """
    
    def __init__(self):
        pass

    def analisar_riscos_oportunidades(self, consulta: str) -> Dict[str, Any]:
        """
        Simula a análise de riscos e oportunidades para missões espaciais.
        """
        print(f"Analisando riscos e oportunidades para: {consulta}")
        riscos = []
        oportunidades = []
        consulta_lower = consulta.lower()

        if "marte" in consulta_lower or "marciana" in consulta_lower:
            riscos.append("Radiação de longa duração e seus efeitos na saúde humana.")
            riscos.append("Dificuldade de pouso e decolagem devido à atmosfera rarefeita.")
            oportunidades.append("Busca por vida passada ou presente.")
            oportunidades.append("Potencial para recursos hídricos e minerais.")
        
        if "lua" in consulta_lower or "lunar" in consulta_lower:
            riscos.append("Poeira lunar abrasiva e seus impactos em equipamentos.")
            riscos.append("Variações extremas de temperatura.")
            oportunidades.append("Base para futuras missões a Marte e além.")
            oportunidades.append("Extração de hélio-3 para energia.")

        if not riscos and not oportunidades:
            riscos.append("Riscos gerais de missões espaciais: falha de equipamento, custos elevados.")
            oportunidades.append("Oportunidades gerais de missões espaciais: avanço científico, desenvolvimento tecnológico.")

        return {"riscos": riscos, "oportunidades": oportunidades}

    def recomendar_investimentos(self, consulta: str) -> List[str]:
        """
        Simula recomendações de investimento em tecnologias espaciais.
        """
        print(f"Recomendando investimentos para: {consulta}")
        recomendacoes = []
        consulta_lower = consulta.lower()

        if "propulsão" in consulta_lower:
            recomendacoes.append("Investir em pesquisa e desenvolvimento de propulsão nuclear térmica.")
        if "habitate" in consulta_lower or "moradia" in consulta_lower:
            recomendacoes.append("Focar em tecnologias de impressão 3D para construção de habitats extraterrestres.")
        if "recursos" in consulta_lower or "mineração" in consulta_lower:
            recomendacoes.append("Apoiar o desenvolvimento de técnicas de mineração de asteroides e recursos in-situ.")
        if "saúde" in consulta_lower or "radiação" in consulta_lower:
            recomendacoes.append("Financiar estudos sobre contramedidas de radiação e saúde de astronautas.")
        
        if not recomendacoes:
            recomendacoes.append("Recomendações gerais: investir em IA para autonomia de missões e robótica avançada.")

        return recomendacoes

    def identificar_tecnologias_promissoras(self, consulta: str) -> List[str]:
        """
        Simula a identificação de tecnologias promissoras.
        """
        print(f"Identificando tecnologias promissoras para: {consulta}")
        tecnologias = []
        consulta_lower = consulta.lower()

        if "marte" in consulta_lower:
            tecnologias.append("Sistemas de suporte de vida de ciclo fechado para Marte.")
            tecnologias.append("Produção de propelente in-situ (ISRU) em Marte.")
        if "lua" in consulta_lower:
            tecnologias.append("Tecnologias de extração de oxigênio do regolito lunar.")
            tecnologias.append("Robótica autônoma para construção lunar.")
        if "viagem" in consulta_lower or "transporte" in consulta_lower:
            tecnologias.append("Propulsão elétrica e iônica de alta eficiência.")
            tecnologias.append("Naves espaciais modulares e reutilizáveis.")
        
        if not tecnologias:
            tecnologias.append("Tecnologias gerais: computação quântica para otimização de trajetórias, nanotecnologia para materiais leves.")

        return tecnologias

    def planejar_missao(self, consulta: str) -> Dict[str, Any]:
        """
        Simula o planejamento de uma missão lunar/marciana.
        """
        print(f"Planejando missão para: {consulta}")
        plano = {"fases": [], "objetivos": [], "recursos_necessarios": []}
        consulta_lower = consulta.lower()

        if "marte" in consulta_lower:
            plano["objetivos"].append("Estabelecer presença humana sustentável em Marte.")
            plano["fases"] = [
                "Fase 1: Reconhecimento e seleção do local de pouso.",
                "Fase 2: Envio de carga e equipamentos robóticos.",
                "Fase 3: Missão tripulada inicial e construção de habitat.",
                "Fase 4: Expansão da base e pesquisa científica."
            ]
            plano["recursos_necessarios"] = [
                "Veículos de lançamento superpesados.",
                "Sistemas de suporte de vida avançados.",
                "Equipamentos de ISRU.",
                "Grandes investimentos financeiros e colaboração internacional."
            ]
        elif "lua" in consulta_lower:
            plano["objetivos"].append("Estabelecer uma base lunar permanente para pesquisa e exploração.")
            plano["fases"] = [
                "Fase 1: Mapeamento detalhado e prospecção de recursos.",
                "Fase 2: Missões robóticas para preparação do local.",
                "Fase 3: Construção de infraestrutura inicial (energia, comunicação).",

                "Fase 4: Missões tripuladas para montagem e operação da base."
            ]
            plano["recursos_necessarios"] = [
                "Módulos habitacionais pré-fabricados.",
                "Robôs de construção autônomos.",
                "Sistemas de energia solar e nuclear.",
                "Parcerias público-privadas."
            ]
        else:
            plano["objetivos"].append("Realizar exploração espacial de forma segura e eficiente.")
            plano["fases"].append("Definição de objetivos e requisitos.")
            plano["fases"].append("Seleção de tecnologias e parceiros.")
            plano["fases"].append("Execução e monitoramento da missão.")
            plano["recursos_necessarios"].append("Equipe multidisciplinar e financiamento adequado.")

        return plano

    def processar_consulta_missoes(self, consulta_texto: str) -> Dict[str, Any]:
        """
        Processa uma consulta relacionada ao planejamento de missões.
        
        Args:
            consulta_texto: A consulta do usuário.
            
        Returns:
            Dicionário com os resultados da análise de missões.
        """
        print(f"Processando consulta de missões: {consulta_texto}")
        
        riscos_oportunidades = self.analisar_riscos_oportunidades(consulta_texto)
        recomendacoes_investimento = self.recomendar_investimentos(consulta_texto)
        tecnologias_promissoras = self.identificar_tecnologias_promissoras(consulta_texto)
        plano_missao = self.planejar_missao(consulta_texto)
        
        return {
            "status": "sucesso",
            "consulta_original": consulta_texto,
            "analise_riscos_oportunidades": riscos_oportunidades,
            "recomendacoes_investimento": recomendacoes_investimento,
            "tecnologias_promissoras": tecnologias_promissoras,
            "plano_missao": plano_missao,
            "mensagem": "Análise de missões concluída com sucesso."
        }

# Exemplo de uso (para teste local)
if __name__ == "__main__":
    agent_missoes = AgentMissoes()
    
    print("\n--- Testando com consulta sobre missão a Marte ---")
    consulta_teste_marte = "Quero planejar uma missão tripulada a Marte"
    resultado_marte = agent_missoes.processar_consulta_missoes(consulta_teste_marte)
    print(json.dumps(resultado_marte, indent=2))

    print("\n--- Testando com consulta sobre base lunar ---")
    consulta_teste_lua = "Quais os riscos e oportunidades de uma base lunar?"
    resultado_lua = agent_missoes.processar_consulta_missoes(consulta_teste_lua)
    print(json.dumps(resultado_lua, indent=2))

    print("\n--- Testando com consulta sobre tecnologias de propulsão ---")
    consulta_teste_tecnologia = "Quais tecnologias de propulsão espacial são promissoras?"
    resultado_tecnologia = agent_missoes.processar_consulta_missoes(consulta_teste_tecnologia)
    print(json.dumps(resultado_tecnologia, indent=2))

    print("\n--- Testando com consulta genérica ---")
    consulta_teste_generica = "Me dê insights para exploração espacial"
    resultado_generica = agent_missoes.processar_consulta_missoes(consulta_teste_generica)
    print(json.dumps(resultado_generica, indent=2))

