# main.py
import argparse
import logging
from pyspark.sql import SparkSession

# Importar funções do nosso pacote wheel
from meu_pacote.utils import criar_spark_session, ler_dados_csv, salvar_como_parquet
from meu_pacote.transformacoes import transformar_colunas_texto, extrair_componentes_data
from meu_pacote.validacoes import validar_valores_nulos

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Processador de dados com wheel')
    parser.add_argument('--input', required=True, help='Caminho de entrada dos dados (S3)')
    parser.add_argument('--output', required=True, help='Caminho de saída para os resultados (S3)')
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info(f"Iniciando processamento: entrada={args.input}, saída={args.output}")
    
    # Criar sessão Spark
    spark = criar_spark_session("Aplicação com Wheel")
    
    try:
        # Ler dados
        df = ler_dados_csv(spark, args.input)
        logger.info(f"Dados carregados: {df.count()} registros")
        
        # Aplicar transformações
        df = transformar_colunas_texto(df, ["produto", "categoria"])
        df = extrair_componentes_data(df, "data_venda")
        
        # Verificar valores nulos
        nulos = validar_valores_nulos(df, ["produto", "valor"])
        for coluna, contagem in nulos.items():
            logger.info(f"Coluna {coluna}: {contagem} valores nulos")
        
        # Salvar resultados
        salvar_como_parquet(df, args.output, particionar_por=["ano", "mes"])
        logger.info(f"Processamento concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()