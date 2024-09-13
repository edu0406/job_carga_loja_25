import boto3
import csv
import sys
from collections import defaultdict

# Parâmetro do nome da pasta, como "fato_vendas"
folder_name = sys.argv[1]

# Nome do arquivo CSV de saída
output_csv = f'list_s3_{folder_name}.csv'

# Configuração da conexão S3
s3 = boto3.client('s3')
bucket_name = 'datalake-edu-teste'

# Dicionário para armazenar os anos e meses encontrados
year_month_dict = defaultdict(set)

# Listando objetos no bucket que correspondem à pasta fornecida
result = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'data/{folder_name}/')

# Processando os objetos para extrair anos e meses
if 'Contents' in result:
    for obj in result['Contents']:
        key = obj['Key']
        # Exemplo de caminho: data/fato_vendas/2022/08/...
        parts = key.split('/')
        if len(parts) >= 4:
            year = parts[2]
            month = parts[3]
            if year.isdigit() and month.isdigit():
                year_month_dict[year].add(month)

# Escrevendo o resultado em um arquivo CSV
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Year', 'Months'])
    for year, months in sorted(year_month_dict.items()):
        csvwriter.writerow([year, ','.join(sorted(months))])

print(f"CSV gerado: {output_csv}")
