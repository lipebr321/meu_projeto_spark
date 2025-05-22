# src/meu_pacote/transformacoes.py
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, upper, to_date, year, month, dayofmonth

def transformar_colunas_texto(df: DataFrame, colunas: list) -> DataFrame:
    """
    Converte colunas de texto para maiúsculas.
    
    Args:
        df: DataFrame do Spark
        colunas: Lista de nomes de colunas para transformar
        
    Returns:
        DataFrame com as colunas transformadas
    """
    for coluna in colunas:
        df = df.withColumn(coluna, upper(col(coluna)))
    return df

def extrair_componentes_data(df: DataFrame, coluna_data: str) -> DataFrame:
    """
    Extrai ano, mês e dia de uma coluna de data.
    
    Args:
        df: DataFrame do Spark
        coluna_data: Nome da coluna de data
        
    Returns:
        DataFrame com colunas adicionais para ano, mês e dia
    """
    return df.withColumn("data_formatada", to_date(col(coluna_data))) \
             .withColumn("ano", year(col("data_formatada"))) \
             .withColumn("mes", month(col("data_formatada"))) \
             .withColumn("dia", dayofmonth(col("data_formatada")))

def calcular_metricas(df: DataFrame, coluna_valor: str) -> DataFrame:
    """
    Calcula métricas adicionais com base em uma coluna de valor.
    
    Args:
        df: DataFrame do Spark
        coluna_valor: Nome da coluna com valores numéricos
        
    Returns:
        DataFrame com colunas adicionais de métricas
    """
    return df.withColumn("valor_com_imposto", col(coluna_valor) * 1.1) \
             .withColumn("valor_com_desconto", col(coluna_valor) * 0.9) \
             .withColumn("valor_arredondado", col(coluna_valor).cast("integer"))