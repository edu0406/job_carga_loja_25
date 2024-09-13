import random
import pandas as pd

# Definindo categorias, nomes de produtos e marcas imaginárias
categories = {
    "Eletrônicos": [
        "Notebook", "Smartphone", "Tablet", "Monitor", "Câmera Digital", 
        "Mouse", "Teclado", "Caixa de Som", "Fone de Ouvido", "Smartwatch"
    ],
    "Perfumaria": [
        "Perfume", "Loção Corporal", "Desodorante", "Sabonete", "Colônia", 
        "Creme Facial", "Óleo Corporal", "Shampoo", "Condicionador", "Sabonete Líquido"
    ],
    "Vestuário": [
        "Camiseta", "Calça Jeans", "Vestido", "Blazer", "Short", 
        "Casaco", "Jaqueta", "Suéter", "Saia", "Bermuda"
    ],
    "Utensílios Domésticos": [
        "Panela", "Prato", "Copo", "Faqueiro", "Assadeira", 
        "Garrafa de água", "Liquidificador", "Frigideira", "Tigela", "Ralador"
    ],
    "Esportivo": [
        "Bicicleta", "Tênis de Corrida", "Raquete de Tênis", "Bola de Futebol", "Mochila Esportiva", 
        "Luvas de Boxe", "Capacete", "Bola de Basquete", "Roupão Esportivo", "Rede de Tênis"
    ]
}

# Marcas com nomes imaginários
brands = [
    "TechNova", "QuantumX", "UltraGlo", "NatureEssence", "ZenithWear", 
    "AeroSport", "EcoHome", "LuxeCraft", "PureScents", "ActivePulse", 
    "FusionGear", "AstraStyle", "MiraBeauty", "EliteFit", "TerraCasa",
    "NovaEdge", "VivaGlam", "PowerMax", "AquaFlow", "SkyLine"
]

# Tamanhos para perfumaria, vestuário e utensílios
sizes = ["Pequeno", "Médio", "Grande", "Extra Grande"]

# Versões para eletrônicos
versions = ["v1.0", "v2.0", "v3.0", "Pro", "Lite"]

# Função para gerar valores de compra e venda
def generate_price():
    purchase_price = round(random.uniform(50, 1000), 2)
    # Em raros casos, valor de venda pode ser menor que o de compra
    if random.random() < 0.05:
        sale_price = round(purchase_price * random.uniform(0.5, 0.9), 2)
    else:
        sale_price = round(purchase_price * random.uniform(1.05, 1.5), 2)
    return purchase_price, sale_price

# Função para gerar lista de produtos únicos
def generate_unique_products(n):
    products = []
    product_id = 90001
    generated_combinations = set()

    while len(products) < n:
        category = random.choice(list(categories.keys()))
        product_name = random.choice(categories[category])
        brand = random.choice(brands)
        
        # Definir tamanho ou versão
        if category in ["Perfumaria", "Vestuário", "Utensílios Domésticos"]:
            size_version = random.choice(sizes)
        else:  # Eletrônicos e Esportivo
            size_version = random.choice(versions)
        
        combination = (product_name, brand, size_version)
        
        # Garantir que a combinação de produto, marca e versão/tamanho seja única
        if combination not in generated_combinations:
            purchase_price, sale_price = generate_price()
            
            products.append({
                "ID_PRODUTO": product_id,
                "NOME_PRODUTO": f"{product_name} ({size_version})",
                "categoria": category,
                "marca": brand,
                "valor de compra": purchase_price,
                "valor de venda": sale_price
            })
            
            generated_combinations.add(combination)
            product_id += 1

    return pd.DataFrame(products)

# Gerando uma lista de 1000 produtos únicos
product_df = generate_unique_products(1000)

# Exibindo o DataFrame gerado
print(product_df)

# Salvando em um arquivo Excel para revisão
product_df.to_excel("product_list_unique_versions_sizes.xlsx", index=False)
