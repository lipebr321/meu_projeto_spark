# src/scripts/processar_dados.py
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
import argparse
import logging
import sys

# Importar módulos do nosso pacote
from meu_pacote.utils import criar_spark_session, ler_dados_csv, salvar_como_parquet
from meu_pacote.transformacoes import transformar_colunas_texto, extrair_componentes_data, calcular_metricas
from meu_pacote.validacoes import validar_schema, validar_valores_nulos

def configurar_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def definir_schema_vendas():
    """Define o schema esperado para os dados de vendas."""
    return StructType([
        StructField("id_venda", StringType(), False),
        StructField("produto", StringType(), True),
        StructField("categoria", StringType(), True),
        StructField("valor", DoubleType(), True),
        StructField("data_venda", StringType(), True),
        StructField("cliente", StringType(), True)
    ])

def processar_dados(input_path, output_path):
    """
    Função principal para processar os dados.
    
    Args:
        input_path: Caminho para os dados de entrada no S3
        output_path: Caminho para salvar os resultados no S3
    """
    logging.info(f"Iniciando processamento de dados")
    logging.info(f"Entrada: {input_path}")
    logging.info(f"Saída: {output_path}")
    
    # Criar sessão Spark
    spark = criar_spark_session("Processamento de Vendas")
    
    try:
        # Ler dados
        df = ler_dados_csv(spark, input_path)
        logging.info(f"Dados carregados com sucesso. Total de registros: {df.count()}")
        
        # Validar schema
        schema_esperado = definir_schema_vendas()
        if not validar_schema(df, schema_esperado):
            logging.warning("O schema dos dados não corresponde ao esperado!")
            logging.info("Schema atual:")
            df.printSchema()
        
        # Verificar valores nulos
        colunas_importantes = ["produto", "valor", "data_venda"]
        nulos = validar_valores_nulos(df, colunas_importantes)
        for coluna, contagem in nulos.items():
            if contagem > 0:
                logging.warning(f"Coluna {coluna} contém {contagem} valores nulos")
        
        # Aplicar transformações
        df_transformado = df
        
        # Transformar texto para maiúsculas
        df_transformado = transformar_colunas_texto(df_transformado, ["produto", "categoria", "cliente"])
        
        # Extrair componentes de data
        df_transformado = extrair_componentes_data(df_transformado, "data_venda")
        
        # Calcular métricas adicionais
        df_transformado = calcular_metricas(df_transformado, "valor")
        
        # Mostrar amostra dos dados processados
        logging.info("Amostra dos dados processados:")
        df_transformado.show(5, truncate=False)
        
        # Salvar resultados
        salvar_como_parquet(
            df_transformado, 
            output_path, 
            particionar_por=["ano", "mes"]
        )
        
        logging.info(f"Processamento concluído com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro durante o processamento: {str(e)}")
        raise
    finally:
        spark.stop()

def main():
    """Função principal que processa argumentos da linha de comando."""
    parser = argparse.ArgumentParser(description='Processador de dados de vendas')
    parser.add_argument('--input', required=True, help='Caminho de entrada dos dados (S3)')
    parser.add_argument('--output', required=True, help='Caminho de saída para os resultados (S3)')
    
    args = parser.parse_args()
    
    configurar_logging()
    processar_dados(args.input, args.output)

if __name__ == "__main__":
    main()