# src/meu_pacote/utils.py
from pyspark.sql import SparkSession, DataFrame
import logging

def criar_spark_session(app_name: str) -> SparkSession:
    """
    Cria uma sessão Spark com configurações otimizadas.
    
    Args:
        app_name: Nome da aplicação
        
    Returns:
        Sessão Spark configurada
    """
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

def ler_dados_csv(spark: SparkSession, caminho: str, tem_cabecalho: bool = True) -> DataFrame:
    """
    Lê dados de um arquivo CSV.
    
    Args:
        spark: Sessão Spark
        caminho: Caminho para o arquivo CSV
        tem_cabecalho: Indica se o CSV tem cabeçalho
        
    Returns:
        DataFrame com os dados do CSV
    """
    return spark.read \
        .option("header", str(tem_cabecalho).lower()) \
        .option("inferSchema", "true") \
        .csv(caminho)

def salvar_como_parquet(df: DataFrame, caminho: str, modo: str = "overwrite", particionar_por: list = None) -> None:
    """
    Salva um DataFrame como arquivo Parquet.
    
    Args:
        df: DataFrame do Spark
        caminho: Caminho para salvar o arquivo
        modo: Modo de escrita (overwrite, append, etc.)
        particionar_por: Lista de colunas para particionar os dados
    """
    writer = df.write.mode(modo)
    
    if particionar_por:
        writer = writer.partitionBy(*particionar_por)
    
    writer.parquet(caminho)
    logging.info(f"Dados salvos com sucesso em: {caminho}")