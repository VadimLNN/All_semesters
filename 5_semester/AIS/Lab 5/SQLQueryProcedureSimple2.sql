CREATE PROCEDURE КакиеПродуктыПриходят
@X varchar(20)=''
AS
SELECT *
FROM Поставщик
WHERE
Тип_продукта = @X