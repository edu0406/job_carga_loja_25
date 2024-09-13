# Loja 25 - Simulação de Dados de uma Loja de Varejo

## Visão Geral
O **Loja 25** é um projeto que simula um ambiente de varejo, gerando dados fictícios para produtos, estoque, clientes, promoções, vendedores e vendas. Ele permite uma análise profunda das operações de uma loja, com tabelas de fato enriquecidas, indicadores de vendas, alertas de estoque e métricas de produtividade de vendedores. O objetivo é demonstrar como a engenharia de dados e a análise podem fornecer insights valiosos em um cenário real de varejo.

---

## Estrutura do Projeto

### Produtos, Estoque e Clientes
O projeto começa com a geração de listas de produtos, níveis de estoque, clientes e dados promocionais.

### Geração Aleatória de Vendas
As vendas são geradas a partir da relação entre vendedores, produtos e a dimensão de tempo, criando um conjunto de dados rico para análise.

### Tabelas de Fato e Enriquecimento
Os dados são consolidados na tabela `fato_vendas`, que é enriquecida com várias dimensões.

### Indicadores de Vendas
Métricas chave de desempenho de vendas são calculadas, incluindo:
- Tendências mensais e anuais de vendas.
- Produtividade de vendedores atuais e ex-funcionários.
- Insights sobre ex-vendedores que poderiam ser recontratados devido ao seu bom desempenho.

---

## Principais Funcionalidades

### Alertas de Estoque:
- **Níveis Baixos/Altos de Estoque**: Identifica produtos com níveis de inventário muito baixos ou muito altos.
- **Análise Custo x Venda**: Sinaliza produtos cujo custo ultrapassa ou está próximo do preço de venda, indicando a necessidade de melhor gerenciamento.

### Produtividade dos Vendedores:
- Acompanha a produtividade de vendedores atuais e ex-funcionários.
- Gera insights sobre a possível recontratação de ex-vendedores com alta performance.

### Relatórios Automáticos:
O projeto gera relatórios em PDF usando Python para várias áreas de negócio:
- Visão Geral do Estoque.
- Indicadores de Vendas.
- Produtividade dos Vendedores.

Esses relatórios são automaticamente enviados por e-mail para as equipes responsáveis.

---

## Fluxo de Dados

### Processo ETL:
- Os dados são processados utilizando **Apache Hop** e armazenados na **AWS S3**.
- O pipeline de dados extrai, transforma e carrega dados de produtos, vendas e vendedores em tabelas de fato e dimensões para análise posterior.

### Relatórios com Python:
- Scripts em Python são usados para analisar os dados e gerar relatórios.
- Cada relatório é personalizado para fornecer insights específicos, como desempenho de vendas e alertas de estoque.

---

## Detalhes Técnicos

- **Apache Hop**: Gerencia o processo ETL e garante o fluxo eficiente dos dados, desde a geração até o armazenamento.
- **AWS S3**: Atua como o armazenamento principal dos dados, abrigando as tabelas de fato enriquecidas e os dados dimensionais.
- **Python**: Responsável pela geração dos relatórios e automação de envio de e-mails.

---

## Casos de Uso

- **Análise de Varejo**: Este projeto pode ser adaptado para ambientes reais de varejo, monitorando o desempenho de vendas, gerenciando o estoque e analisando a produtividade dos vendedores.
- **Simulação de Dados**: Serve como uma ferramenta útil para simular operações de varejo em larga escala, oferecendo insights sobre o tratamento, enriquecimento e relatórios de dados.
