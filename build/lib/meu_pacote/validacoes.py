# src/meu_pacote/validacoes.py
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

def validar_schema(df: DataFrame, schema_esperado: StructType) -> bool:
    """
    Valida se o DataFrame possui o schema esperado.
    
    Args:
        df: DataFrame do Spark
        schema_esperado: Schema esperado
        
    Returns:
        True se o schema for válido, False caso contrário
    """
    return df.schema == schema_esperado

def validar_valores_nulos(df: DataFrame, colunas: list) -> dict:
    """
    Verifica se existem valores nulos nas colunas especificadas.
    
    Args:
        df: DataFrame do Spark
        colunas: Lista de nomes de colunas para verificar
        
    Returns:
        Dicionário com contagem de nulos por coluna
    """
    resultado = {}
    for coluna in colunas:
        contagem = df.filter(df[coluna].isNull()).count()
        resultado[coluna] = contagem
    return resultado

def validar_intervalo_valores(df: DataFrame, coluna: str, min_valor: float, max_valor: float) -> bool:
    """
    Verifica se todos os valores de uma coluna estão dentro de um intervalo.
    
    Args:
        df: DataFrame do Spark
        coluna: Nome da coluna para verificar
        min_valor: Valor mínimo aceitável
        max_valor: Valor máximo aceitável
        
    Returns:
        True se todos os valores estiverem no intervalo, False caso contrário
    """
    fora_intervalo = df.filter((col(coluna) < min_valor) | (col(coluna) > max_valor)).count()
    return fora_intervalo == 0