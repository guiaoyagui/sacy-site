import requests
from bs4 import BeautifulSoup
from ddgs import DDGS  # DuckDuckGo Search API Wrapper


class AgentLiteratura:
    def __init__(self):
        self.ddgs = DDGS()

    def buscar_e_resumir(self, consulta: str) -> str:
        try:
            print(f"🔍 Buscando resultados para: {consulta}")

            resultados = list(self.ddgs.text(consulta, max_results=3))
            if not resultados:
                return "⚠️ Nenhum resultado encontrado."

            top_resultado = resultados[0]
            titulo = top_resultado.get("title", "Sem título")
            link = top_resultado.get("href", "#")
            descricao = top_resultado.get("body", "")

            html = self._obter_conteudo_pagina(link)
            resumo = self._gerar_resumo(html)

            if not resumo or len(resumo.strip()) < 30:
                resumo = descricao or "⚠️ Não foi possível gerar um resumo relevante."

            imagens = self._buscar_imagens(consulta)

            imagens_html = "".join([
                f"<img src='{img}' width='300' style='border-radius:12px;margin:8px;"
                f"box-shadow:0 2px 8px rgba(0,0,0,0.3);object-fit:cover;'>"
                for img in imagens
            ]) if imagens else "<p style='color:#999;'>⚠️ Nenhuma imagem encontrada.</p>"

            resposta_html = f"""
<div style='font-family:Inter, sans-serif; color:#f1f1f1;'>
  <h2 style='color:#7dd3fc;display:flex;align-items:center;gap:6px;'>🧠 Resumo Educacional</h2>
  <p style='font-size:15px;margin-top:4px;'><b>Tópico:</b> {consulta}</p>

  <h3 style='color:#93c5fd;margin-top:10px;'>📄 {titulo}</h3>
  <p style='font-size:15px;line-height:1.7;color:#d1d5db;margin-top:6px;text-align:justify;'>
    {resumo}
  </p>

  <a href='{link}' target='_blank' style='display:inline-block;margin-top:12px;color:#38bdf8;
  text-decoration:none;font-weight:500;'>📘 Ler artigo completo</a>

  <hr style='margin:16px 0;border-color:#333;'>

  <h3 style='color:#7dd3fc;margin-bottom:6px;'>🖼️ Imagens relacionadas:</h3>
  <div style='display:flex;flex-wrap:wrap;gap:10px;justify-content:center;'>{imagens_html}</div>
</div>
"""
            return resposta_html.strip()

        except Exception as e:
            print(f"❌ Erro em buscar_e_resumir: {e}")
            return f"❌ Erro ao processar consulta: {str(e)}"

    def _obter_conteudo_pagina(self, url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"⚠️ Erro ao obter conteúdo de {url}: {e}")
            return ""

    def _gerar_resumo(self, html: str) -> str:
        """Extrai texto e gera um resumo curto e didático."""
        if not html:
            return ""

        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            texto = soup.get_text(separator=" ", strip=True)
            texto = " ".join(texto.split())

            if len(texto) < 200:
                return ""

            # Quebrar o texto em frases
            frases = texto.split(". ")

            # Escolher apenas as 3-4 primeiras frases mais relevantes
            resumo = ". ".join(frases[:4]) + "."

            # Simplificar o texto para leitura de estudante
            resumo = resumo.replace("porém", "mas").replace("todavia", "mas")
            resumo = resumo.replace("dessa forma", "assim").replace("portanto", "então")

            # Ajuste final de clareza
            resumo += " Este resumo tem o objetivo de te ajudar a compreender o tema de forma rápida e clara. ✨"

            return resumo

        except Exception as e:
            print(f"⚠️ Erro ao gerar resumo: {e}")
            return ""

    def _buscar_imagens(self, consulta: str):
        """Busca imagens: tenta DDGS, depois Google."""
        imagens = []

        try:
            for img in self.ddgs.images(consulta, max_results=5):
                url = img.get("image")
                if url and url.startswith("http"):
                    imagens.append(url)
                if len(imagens) >= 3:
                    return imagens
        except Exception as e:
            print(f"⚠️ Erro DDGS imagens: {e}")

        try:
            print("🔄 Tentando buscar imagens no Google...")
            headers = {"User-Agent": "Mozilla/5.0"}
            url = f"https://www.google.com/search?tbm=isch&q={consulta}"
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for img_tag in soup.find_all("img"):
                src = img_tag.get("src")
                if src and src.startswith("http"):
                    imagens.append(src)
                if len(imagens) >= 3:
                    break
        except Exception as e:
            print(f"⚠️ Erro ao buscar imagens no Google: {e}")

        return imagens[:3]
