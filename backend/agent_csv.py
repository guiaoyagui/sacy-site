#!/usr/bin/env python3
"""
Agent Especialista em CSV (Data Analyst)
Análise de dados estruturados
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os
import json
import numpy as np
from typing import Dict, Any, List, Optional

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class AgentCSV:
    """
    Agent Especialista em CSV - Análise de dados estruturados
    
    Responsabilidades:
    - Processamento de arquivos CSV da NASA
    - Análise estatística e exploratória
    - Identificação de padrões e tendências
    - Geração de visualizações
    """
    
    def __init__(self):
        self.data_dir = "/home/ubuntu/data_csv"
        os.makedirs(self.data_dir, exist_ok=True)

    def download_csv(self, url: str, filename: str) -> str:
        """
        Faz o download de um arquivo CSV de uma URL e o salva localmente.
        
        Args:
            url: URL do arquivo CSV.
            filename: Nome do arquivo para salvar localmente.
            
        Returns:
            Caminho completo para o arquivo salvo.
        
        Raises:
            requests.exceptions.RequestException: Se houver um erro no download.
        """
        filepath = os.path.join(self.data_dir, filename)
        print(f"Tentando baixar CSV de: {url} para {filepath}")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status() # Levanta um HTTPError para requisições HTTP ruins (4xx ou 5xx)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Download concluído: {filepath}")
            return filepath
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar o arquivo CSV de {url}: {e}")
            raise

    def carregar_csv(self, filepath: str) -> pd.DataFrame:
        """
        Carrega um arquivo CSV em um DataFrame do pandas.
        
        Args:
            filepath: Caminho para o arquivo CSV.
            
        Returns:
            DataFrame do pandas.
        
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado.
            pd.errors.EmptyDataError: Se o arquivo CSV estiver vazio.
            pd.errors.ParserError: Se houver um erro de parsing no CSV.
        """
        print(f"Carregando arquivo CSV: {filepath}")
        try:
            df = pd.read_csv(filepath)
            print(f"CSV carregado com sucesso. Formato: {df.shape}")
            return df
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em {filepath}")
            raise
        except pd.errors.EmptyDataError:
            print(f"Erro: Arquivo CSV vazio em {filepath}")
            raise
        except pd.errors.ParserError as e:
            print(f"Erro de parsing no arquivo CSV {filepath}: {e}")
            raise

    def analisar_dados(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Realiza uma análise estatística e exploratória básica dos dados.
        
        Args:
            df: DataFrame do pandas.
            
        Returns:
            Dicionário com os resultados da análise.
        """
        print("Realizando análise de dados...")
        analise = {
            "colunas": df.columns.tolist(),
            "tipos_dados": df.dtypes.astype(str).to_dict(),
            "estatisticas_descritivas": df.describe(include='all').to_dict(),
            "valores_ausentes": df.isnull().sum().to_dict(),
            "linhas_duplicadas": df.duplicated().sum()
        }
        print("Análise de dados concluída.")
        return analise

    def gerar_visualizacao(self, df: pd.DataFrame, column: str, plot_type: str = 'hist') -> str:
        """
        Gera uma visualização para uma coluna específica e salva como imagem.
        
        Args:
            df: DataFrame do pandas.
            column: Nome da coluna para visualizar.
            plot_type: Tipo de plotagem ('hist', 'box', 'scatter').
            
        Returns:
            Caminho para o arquivo de imagem gerado.
        
        Raises:
            ValueError: Se a coluna não existir ou o tipo de plotagem for inválido.
        """
        if column not in df.columns:
            raise ValueError(f"Coluna '{column}' não encontrada no DataFrame.")
        
        output_filename = os.path.join(self.data_dir, f"plot_{column}_{plot_type}.png")
        plt.figure(figsize=(10, 6))
        
        if plot_type == 'hist':
            if pd.api.types.is_numeric_dtype(df[column]):
                sns.histplot(df[column].dropna(), kde=True)
                plt.title(f'Distribuição de {column}')
                plt.xlabel(column)
                plt.ylabel('Frequência')
            else:
                df[column].value_counts().plot(kind='bar')
                plt.title(f'Contagem de {column}')
                plt.xlabel(column)
                plt.ylabel('Contagem')
        elif plot_type == 'box':
            if pd.api.types.is_numeric_dtype(df[column]):
                sns.boxplot(y=df[column].dropna())
                plt.title(f'Box Plot de {column}')
                plt.ylabel(column)
            else:
                raise ValueError(f"Box plot não é adequado para coluna não numérica '{column}'.")
        elif plot_type == 'scatter':
            # Scatter plot requer duas colunas, aqui faremos um exemplo simples com índice
            if pd.api.types.is_numeric_dtype(df[column]):
                plt.scatter(df.index, df[column])
                plt.title(f'Scatter Plot de {column}')
                plt.xlabel('Índice')
                plt.ylabel(column)
            else:
                raise ValueError(f"Scatter plot não é adequado para coluna não numérica '{column}'.")
        else:
            raise ValueError(f"Tipo de plotagem '{plot_type}' inválido. Escolha entre 'hist', 'box', 'scatter'.")

        plt.tight_layout()
        plt.savefig(output_filename)
        plt.close()
        print(f"Visualização gerada: {output_filename}")
        return output_filename

    def processar_consulta_csv(self, consulta_texto: str, csv_url: Optional[str] = None, csv_filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Processa uma consulta relacionada a dados CSV.
        
        Args:
            consulta_texto: A consulta do usuário.
            csv_url: URL do arquivo CSV para download (opcional).
            csv_filepath: Caminho local para o arquivo CSV (opcional).
            
        Returns:
            Dicionário com os resultados da análise e caminhos para visualizações.
        """
        df = None
        if csv_url:
            try:
                downloaded_path = self.download_csv(csv_url, os.path.basename(csv_url))
                df = self.carregar_csv(downloaded_path)
            except Exception as e:
                return {"status": "erro", "mensagem": f"Falha ao processar CSV da URL: {e}"}
        elif csv_filepath:
            try:
                df = self.carregar_csv(csv_filepath)
            except Exception as e:
                return {"status": "erro", "mensagem": f"Falha ao processar CSV do arquivo local: {e}"}
        else:
            return {"status": "erro", "mensagem": "Nenhuma URL ou caminho de arquivo CSV fornecido."}

        if df is None:
            return {"status": "erro", "mensagem": "Não foi possível carregar o DataFrame."}

        analise_resultados = self.analisar_dados(df)
        visualizacoes = []

        # Tentar gerar visualizações para colunas numéricas ou categóricas
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                try:
                    visualizacoes.append(self.gerar_visualizacao(df, col, 'hist'))
                    visualizacoes.append(self.gerar_visualizacao(df, col, 'box'))
                except ValueError as e:
                    print(f"Não foi possível gerar visualização para {col}: {e}")
            elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
                # Para colunas categóricas, podemos gerar um histograma de contagem
                try:
                    visualizacoes.append(self.gerar_visualizacao(df, col, 'hist'))
                except ValueError as e:
                    print(f"Não foi possível gerar visualização para {col}: {e}")

        return {
            "status": "sucesso",
            "consulta_original": consulta_texto,
            "analise": analise_resultados,
            "visualizacoes": visualizacoes,
            "mensagem": "Análise CSV concluída com sucesso."
        }

# Exemplo de uso (para teste local)
if __name__ == "__main__":
    agent_csv = AgentCSV()
    
    # Exemplo de URL de CSV do GitHub (SB_publication_PMC.csv)
    github_csv_url = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"
    
    print("\n--- Testando com CSV do GitHub ---")
    try:
        resultado_github = agent_csv.processar_consulta_csv(
            consulta_texto="Analise o CSV de publicações do GitHub",
            csv_url=github_csv_url
        )
        print(json.dumps(resultado_github, indent=2, cls=NumpyEncoder))
    except Exception as e:
        print(f"Erro no teste do CSV do GitHub: {e}")

    # Exemplo de CSV local (simulado para teste)
    print("\n--- Testando com CSV local (simulado) ---")
    dummy_csv_path = os.path.join(agent_csv.data_dir, "dummy_data.csv")
    with open(dummy_csv_path, "w") as f:
        f.write("id,valor,categoria\n1,10,A\n2,20,B\n3,15,A\n4,25,C\n5,12,B")
    
    try:
        resultado_local = agent_csv.processar_consulta_csv(
            consulta_texto="Analise o CSV de dados simulados",
            csv_filepath=dummy_csv_path
        )
        print(json.dumps(resultado_local, indent=2, cls=NumpyEncoder))
    except Exception as e:
        print(f"Erro no teste do CSV local: {e}")

    # Limpar arquivos gerados (opcional)
    # import shutil
    # shutil.rmtree(agent_csv.data_dir)
    # print(f"Diretório {agent_csv.data_dir} removido.")

