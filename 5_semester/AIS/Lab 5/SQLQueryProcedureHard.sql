CREATE PROCEDURE ���������������������������
@X INTEGER 
AS
SELECT * FROM ���������
WHERE id IN (
        SELECT ���������_id FROM ���� WHERE ���� > @X
    );