# 🧠 Sacy AI — Sistema de Roteamento Inteligente de Agentes  
**Transformando informação em conhecimento**

---

## 🚀 Visão Geral

O **Sacy AI** é um sistema educacional inteligente projetado para **revolucionar o aprendizado dos estudantes do ENEM**.  
Com base em **IA generativa** e **algoritmos de grafos**, o sistema oferece respostas didáticas, personalizadas e contextualizadas, garantindo uma experiência de aprendizado mais eficaz e acessível.

---

## 🎯 Objetivo

> Otimizar o processo de aprendizado, adaptando-se às necessidades individuais de cada aluno, através de inteligência artificial e roteamento automatizado de consultas.

---

## 🧩 Principais Funcionalidades

### 📘 Respostas Didáticas  
Geração de conteúdo adaptado ao nível de conhecimento do aluno, com explicações detalhadas e exemplos práticos.

### 🔍 Busca Inteligente  
Integração com **Gemini + DDGS**, fornecendo informações atualizadas e confiáveis com grounding em fontes verificadas.

### 🖼️ Geração de Imagens  
Criação automática de recursos visuais para apoiar o aprendizado de conceitos complexos.

### 🧭 Roteamento Automático  
Direcionamento inteligente das consultas para **agentes especializados**, garantindo respostas de quem tem expertise na área.

---

## 🏗️ Arquitetura do Sistema

O Sacy AI é composto por **cinco camadas integradas**, garantindo respostas precisas e personalizadas:

| Camada | Função |
|--------|--------|
| **1. API Flask** | Orquestra requisições e coordena a comunicação entre módulos |
| **2. Classificador Gemini** | Analisa consultas e identifica a categoria do tema com alta precisão |
| **3. Roteador de Agentes** | Utiliza algoritmos de grafos para direcionar a consulta ao agente correto |
| **4. Agentes Especializados** | Seis áreas do conhecimento do ENEM: Exatas, Literatura, Química, Geografia, Redação e Arte |
| **5. Ferramentas Auxiliares** | Busca Web, Wikipedia API e geração de imagens educativas |

---

## 🔢 Algoritmo de Grafos

O núcleo do sistema é um **Grafo Direcionado Acíclico (DAG)** que garante **roteamento eficiente e sem redundância**.

- **Nós (Vértices):** Representam os agentes especializados  
- **Arestas (Conexões):** Determinam as rotas entre a classificação e os agentes  
- **Propriedade:** Cada consulta percorre **um único caminho** até o agente ideal  

---

## ⚙️ Fluxo de Processamento

1. **Recepção da Consulta**  
   O aluno envia uma pergunta via API Flask.  
   ```python
   consulta = "O que é a Segunda Lei de Newton?"
   ```

2. **Classificação com Gemini**  
   O modelo Gemini 2.5 Flash identifica a categoria:
   ```python
   categoria = "FISICA"
   ```

3. **Roteamento Inteligente**  
   O sistema mapeia a categoria e seleciona o agente especializado:
   ```python
   if categoria in ["MATEMATICA", "FISICA"]:
       return agente_modo_exatas(consulta)
   ```

4. **Geração da Resposta**  
   O agente cria uma explicação didática, formatada em **HTML** com:
   - Definição clara  
   - Fórmulas e exemplos  
   - Relevância para o ENEM  

🕒 Tempo médio total: **~1.5 segundos**

---

## 🧑‍🏫 Agentes Especializados

| Agente | Áreas | Status |
|--------|--------|--------|
| 🧮 **Exatas** | Matemática, Física | ✅ Implementado |
| 📚 **Literatura** | Literatura, História | ✅ Implementado |
| ⚗ **Química** | Química | ✅ Implementado |
| 🌍 **Geografia** | Geografia | ✅ Implementado |
| ✍ **Redação** | Redação ENEM | ✅ Implementado |
| 🎨 **Arte** | Artes Visuais | 🕓 Em Desenvolvimento |

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|------------|--------------|
| **Backend** | Flask (Python) |
| **IA Generativa** | Google Gemini 2.5 Flash |
| **Busca Web** | Gemini + DuckDuckGo Search (DDGS) |
| **Banco de Dados** | Wikipedia API |
| **Frontend** | HTML / CSS / JavaScript |
| **Integração** | CORS + REST API |

---

## 🧮 Estrutura do Grafo

- **Tipo:** Grafo Direcionado Acíclico (DAG)  
- **Nós:** Classificador + 6 Agentes  
- **Arestas:** Conexões de roteamento direto  
- **Propriedade:** Caminho único por consulta  
- **Benefícios:**  
  - Sem redundância  
  - Fácil manutenção  
  - Previsibilidade no processamento

---

## 🧩 Resultados Alcançados

| Métrica | Resultado |
|----------|------------|
| ⚡ **Performance** | Tempo médio < 2 segundos |
| 🎯 **Precisão** | >95% de acerto na classificação |
| 🤖 **Cobertura** | 6 áreas do ENEM |
| 📚 **Qualidade** | Respostas didáticas em HTML |
| 🔗 **Integração** | APIs externas 100% funcionais |

---

## 🚧 Próximos Passos

- 🎨 Finalizar **Agente de Arte**
- 💬 Sistema de **feedback** dos estudantes
- 📊 Implementar **métricas e analytics**
- 📖 Expandir conteúdos e disciplinas
- 🎮 Introduzir **gamificação** para engajamento

---

## 🧠 Conclusão

O **Sacy AI** demonstra o poder da combinação entre **IA generativa**, **algoritmos de grafos** e **design educacional inteligente**.  
Mais que um projeto acadêmico, é um passo em direção à **democratização do acesso à educação de qualidade**.

---

## 🖥️ Execução Local

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/<nome-do-repositorio>.git

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o servidor Flask
python app.py

# 4. Acesse no navegador
http://localhost:5000
```
