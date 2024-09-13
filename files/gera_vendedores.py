import random
import pandas as pd
from datetime import datetime, timedelta

# Função para gerar uma data de admissão aleatória
def generate_random_date(start_date, end_date):
    if start_date > end_date:
        return start_date  # Garante que a data de retorno seja a data de início, evitando erro
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Função para calcular o salário baseado no nível hierárquico
def calculate_salary(category):
    base_salary = {
        "junior-1": 1500,
        "junior-2": 2000,
        "pleno-1": 2500,
        "pleno-2": 3000,
        "pleno-3": 3500,
        "senior-1": 4000,
        "senior-2": 4500,
        "senior-3": 5000,
        "senior-4": 5490
    }
    return base_salary[category] + random.uniform(0, 500)

# Função para gerar um nível hierárquico baseado no tempo de casa
def determine_category(years):
    if years <= 1:
        return "junior-1"
    elif years <= 3:
        return "junior-2"
    elif years <= 5:
        return "pleno-1"
    elif years <= 7:
        return "pleno-2"
    elif years <= 10:
        return "pleno-3"
    elif years <= 12:
        return "senior-1"
    elif years <= 15:
        return "senior-2"
    elif years <= 20:
        return "senior-3"
    else:
        return "senior-4"

# Lista ampliada de nomes
male_names = ["Rafael", "Lucas", "José", "Carlos", "Pedro", "Thiago", "Marcelo", "Bruno", "Gustavo", "Felipe",
              "João", "Miguel", "Gabriel", "Daniel", "Rodrigo", "Mateus", "André", "Alexandre", "Leonardo", "Henrique",
              "Eduardo", "Paulo", "Victor", "Rogério", "Rafael", "Fernando", "Ricardo", "Vinícius", "Antônio", "Juliano"]

female_names = ["Ana", "Maria", "Juliana", "Carla", "Fernanda", "Paula", "Renata", "Beatriz", "Amanda", "Sabrina",
                "Claudia", "Isabela", "Camila", "Larissa", "Patrícia", "Mariana", "Luciana", "Carolina", "Tatiana", "Elaine",
                "Vanessa", "Cintia", "Raquel", "Helena", "Simone", "Roberta", "Bianca", "Cristina", "Sandra", "Aline"]

surnames = ["Costa", "Nascimento", "Pereira", "Silva", "Souza", "Mendes", "Almeida", "Rodrigues", "Ferreira", "Martins",
            "Oliveira", "Santos", "Gomes", "Barbosa", "Ribeiro", "Dias", "Correia", "Moreira", "Teixeira", "Vieira",
            "Lima", "Araújo", "Carvalho", "Ramos", "Batista", "Borges", "Morais", "Moraes", "Neves", "Cardoso"]

# Função para gerar o dataset dos vendedores
def generate_sellers_dataset(start_year=2010, end_year=2024, initial_count=5):
    matricula = 7001
    sellers = []
    current_sellers = initial_count
    
    names = male_names + female_names

    for year in range(start_year, end_year + 1):
        variation = random.uniform(-0.2, 0.4)  # Variar entre -20% e +40%
        new_sellers_count = max(1, int(current_sellers * (1 + variation)))
        
        for _ in range(new_sellers_count):
            name = random.choice(names)
            surname = random.choice(surnames)
            admission_date = generate_random_date(datetime(year, 1, 1), datetime(year, 12, 31))
            time_with_company = (datetime.now() - admission_date).days // 365
            category = determine_category(time_with_company)
            salary = calculate_salary(category)
            
            if random.random() < 0.6:  # 60% de chance de demissão
                dismissal_date = generate_random_date(admission_date, datetime.now())
                if (datetime.now() - admission_date).days > 6 * 365 or dismissal_date > datetime.now():
                    dismissal_date = datetime.now()
            else:
                dismissal_date = ""

            sellers.append({
                "Matricula": matricula,
                "Nome": name,
                "Sobrenome": surname,
                "Data De Admissão": admission_date.strftime('%d/%m/%Y'),
                "Data de Demissão": dismissal_date.strftime('%d/%m/%Y') if dismissal_date else "",
                "Categoria": category,
                "Salário": round(salary, 2)
            })
            matricula += 1
        
        current_sellers = new_sellers_count

    return pd.DataFrame(sellers)

# Gerar o dataset garantindo 5 vendedores no início
def initialize_sellers(start_date, initial_count=5):
    matricula = 7001
    sellers = []
    
    names = male_names + female_names

    for _ in range(initial_count):
        name = random.choice(names)
        surname = random.choice(surnames)
        admission_date = generate_random_date(start_date, start_date)
        category = determine_category(0)
        salary = calculate_salary(category)
        
        # Randomizar demissões para vendedores iniciais também
        if random.random() < 0.5:  # 50% de chance de demissão para vendedores iniciais
            dismissal_date = generate_random_date(admission_date, datetime(2024, 8, 14))  # Até a data atual
        else:
            dismissal_date = ""

        sellers.append({
            "Matricula": matricula,
            "Nome": name,
            "Sobrenome": surname,
            "Data De Admissão": admission_date.strftime('%d/%m/%Y'),
            "Data de Demissão": dismissal_date.strftime('%d/%m/%Y') if dismissal_date else "",
            "Categoria": category,
            "Salário": round(salary, 2)
        })
        matricula += 1
    
    return pd.DataFrame(sellers)

# Iniciando os primeiros 5 vendedores em 01/01/2010
start_date = datetime(2010, 1, 1)
initial_sellers_df = initialize_sellers(start_date)

# Gerando os vendedores dos anos subsequentes até 2024
additional_sellers_df = generate_sellers_dataset()

# Concatenando os dois datasets
sellers_df = pd.concat([initial_sellers_df, additional_sellers_df], ignore_index=True)

# Ajustando a hierarquia e salários de acordo com a antiguidade
sellers_df.sort_values(by=['Data De Admissão'], inplace=True)
for idx, seller in sellers_df.iterrows():
    time_with_company = (datetime.now() - datetime.strptime(seller['Data De Admissão'], '%d/%m/%Y')).days // 365
    sellers_df.at[idx, 'Categoria'] = determine_category(time_with_company)
    sellers_df.at[idx, 'Salário'] = round(calculate_salary(sellers_df.at[idx, 'Categoria']), 2)

# Exibindo o dataset final
print(sellers_df)

# Salvando em um arquivo Excel para revisão
sellers_df.to_excel("vendedores.xlsx", index=False)
