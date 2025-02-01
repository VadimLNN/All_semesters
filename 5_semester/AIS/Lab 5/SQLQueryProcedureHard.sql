CREATE PROCEDURE СотрудникиСБлюдамиДорожеЧем
@X INTEGER 
AS
SELECT * FROM Сотрудник
WHERE id IN (
        SELECT Сотрудник_id FROM Меню WHERE Цена > @X
    );