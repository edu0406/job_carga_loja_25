CREATE PROCEDURE dbo.GerarVendas(
    @ANO INT,
    @QuantidadeRegistros INT
)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Contador INT = 0;
    DECLARE @DataVenda DATE;
    DECLARE @Mes INT;
    DECLARE @MatriculaVendedor INT;
    DECLARE @MatriculaCliente INT;
    DECLARE @IDProduto INT;
    DECLARE @Avaliacao INT;
    DECLARE @QtdComprada INT;

    -- Tabela temporária para armazenar as vendas
    CREATE TABLE #Vendas
    (
        DATA_VENDA DATE,
        MATRICULA_VENDEDOR INT,
        MATRICULA_CLIENTE INT,
        ID_PRODUTO INT,
        AVALIACAO INT,
        QTD_COMPRADA INT
    );

    -- Tabela temporária para armazenar as datas com a tendência
    CREATE TABLE #DatasTendencia
    (
        SK_DATA DATE,
        Mes INT,
        RN INT
    );

    -- Inserir todas as datas do ano
    INSERT INTO #DatasTendencia (SK_DATA, Mes, RN)
    SELECT SK_DATA, MONTH(SK_DATA),
           ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RN
    FROM DIM.dbo.DIM_TEMPO
    WHERE ANO = @ANO;

    -- Tabela temporária para armazenar os vendedores ativos
    CREATE TABLE #VendedoresAtivos
    (
        MATRICULA INT,
        RN INT
    );

    INSERT INTO #VendedoresAtivos (MATRICULA, RN)
    SELECT DISTINCT v.MATRICULA, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RN
    FROM STG.dbo.LOJA_25_VENDEDORES v
    INNER JOIN DIM.dbo.DIM_TEMPO t
        ON t.SK_DATA BETWEEN v.DATA_ADMISSAO AND ISNULL(v.DATA_DEMISSAO, t.SK_DATA)
    WHERE t.ANO = @ANO AND (t.DIA_UTIL = 1 OR t.DIA_SEMANA_NUM = 7);

    -- Contagem total de registros disponíveis
    DECLARE @TotalDatas INT, @TotalVendedores INT;
    SELECT @TotalDatas = MAX(RN) FROM #DatasTendencia;
    SELECT @TotalVendedores = MAX(RN) FROM #VendedoresAtivos;

    -- Distribuição básica: gera vendas distribuídas por todos os meses
    WHILE @Contador < (@QuantidadeRegistros * 0.65)  -- 65% das vendas distribuídas uniformemente
    BEGIN
        -- Seleciona uma data aleatória de qualquer mês
        DECLARE @RandomDateIndex1 INT = FLOOR(RAND() * @TotalDatas) + 1;
        SELECT @DataVenda = SK_DATA, @Mes = Mes
        FROM #DatasTendencia
        WHERE RN = @RandomDateIndex1;

        -- Seleciona um vendedor aleatório
        DECLARE @RandomVendedorIndex1 INT = FLOOR(RAND() * @TotalVendedores) + 1;
        SELECT @MatriculaVendedor = MATRICULA
        FROM #VendedoresAtivos
        WHERE RN = @RandomVendedorIndex1;

        -- Gera a avaliação com base no mês
        IF @Mes BETWEEN 2 AND 8  -- Fevereiro a Agosto
            SET @Avaliacao = FLOOR(RAND() * (10 - 7 + 1)) + 7; -- Avaliação privilegiando entre 7 e 10
        ELSE  -- Restante do ano
            SET @Avaliacao = FLOOR(RAND() * (7 - 4 + 1)) + 4; -- Avaliação privilegiando entre 4 e 7

        -- Gera valores aleatórios para as outras colunas
        SET @MatriculaCliente = FLOOR(RAND() * (11000 - 10001 + 1)) + 10001; -- Cliente entre 10001 e 11000
        SET @IDProduto = FLOOR(RAND() * (91000 - 90001 + 1)) + 90001; -- Produto entre 90001 e 91000
        SET @QtdComprada = FLOOR(RAND() * (5 - 1 + 1)) + 1; -- Quantidade comprada entre 1 e 5

        -- Insere o registro na tabela temporária
        INSERT INTO #Vendas (DATA_VENDA, MATRICULA_VENDEDOR, MATRICULA_CLIENTE, ID_PRODUTO, AVALIACAO, QTD_COMPRADA)
        VALUES (@DataVenda, @MatriculaVendedor, @MatriculaCliente, @IDProduto, @Avaliacao, @QtdComprada);

        SET @Contador = @Contador + 1;
    END

    -- Aumento nos meses finais: gera mais vendas de setembro a dezembro
    WHILE @Contador < @QuantidadeRegistros  -- 35% das vendas concentradas nos últimos meses
    BEGIN
        -- Seleciona uma data aleatória dos meses de setembro a dezembro
        DECLARE @RandomDateIndex2 INT = FLOOR(RAND() * (@TotalDatas * 0.35)) + (@TotalDatas * 0.65);
        SELECT @DataVenda = SK_DATA, @Mes = Mes
        FROM #DatasTendencia
        WHERE RN = @RandomDateIndex2 AND Mes BETWEEN 9 AND 12;

        -- Seleciona um vendedor aleatório
        DECLARE @RandomVendedorIndex2 INT = FLOOR(RAND() * @TotalVendedores) + 1;
        SELECT @MatriculaVendedor = MATRICULA
        FROM #VendedoresAtivos
        WHERE RN = @RandomVendedorIndex2;

        -- Gera a avaliação com base no mês
        SET @Avaliacao = FLOOR(RAND() * (7 - 4 + 1)) + 4; -- Avaliação privilegiando entre 4 e 7

        -- Gera valores aleatórios para as outras colunas
        SET @MatriculaCliente = FLOOR(RAND() * (11000 - 10001 + 1)) + 10001; -- Cliente entre 10001 e 11000
        SET @IDProduto = FLOOR(RAND() * (91000 - 90001 + 1)) + 90001; -- Produto entre 90001 e 91000
        SET @QtdComprada = FLOOR(RAND() * (5 - 1 + 1)) + 1; -- Quantidade comprada entre 1 e 5

        -- Insere o registro na tabela temporária
        INSERT INTO #Vendas (DATA_VENDA, MATRICULA_VENDEDOR, MATRICULA_CLIENTE, ID_PRODUTO, AVALIACAO, QTD_COMPRADA)
        VALUES (@DataVenda, @MatriculaVendedor, @MatriculaCliente, @IDProduto, @Avaliacao, @QtdComprada);

        SET @Contador = @Contador + 1;
    END

    -- Retorna os resultados
    SELECT * FROM #Vendas;

    -- Limpa as tabelas temporárias
    DROP TABLE #Vendas;
    DROP TABLE #DatasTendencia;
    DROP TABLE #VendedoresAtivos;
END;