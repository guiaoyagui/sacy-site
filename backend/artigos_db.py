# backend/artigos_db.py
import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("Ficheiro .env encontrado e carregado.")
else:
    print("AVISO: Ficheiro .env não encontrado.")

class ArtigosDB:
    def _get_connection(self):
        try:
            connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            return connection
        except psycopg2.OperationalError as e:
            print(f"ERRO CRÍTICO: Não foi possível conectar ao PostgreSQL: {e}")
            return None

    def buscar_artigos(self, termo_busca: str):
        connection = self._get_connection()
        if not connection:
            return []

        # --- MELHORIA AQUI: Busca por palavras-chave ---
        palavras_chave = [palavra for palavra in termo_busca.split() if len(palavra) > 3]
        if not palavras_chave:
            return []

        # Constrói a cláusula WHERE dinamicamente
        clausulas_where = " OR ".join(["(assunto ILIKE %s OR mini_resumo ILIKE %s)" for _ in palavras_chave])
        query = f"SELECT assunto, link, mini_resumo FROM conhecimentos WHERE {clausulas_where};"
        
        # Cria a lista de parâmetros para a query
        params = []
        for palavra in palavras_chave:
            termo_like = f"%{palavra}%"
            params.extend([termo_like, termo_like])

        results = []
        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute(query, tuple(params))
                    print(f"Encontrados {cur.rowcount} artigos para as palavras-chave: {palavras_chave}.")
                    for row in cur.fetchall():
                        results.append({
                            "titulo": row[0],
                            "link": row[1],
                            "abstract": row[2]
                        })
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
        
        return results

db = ArtigosDB()