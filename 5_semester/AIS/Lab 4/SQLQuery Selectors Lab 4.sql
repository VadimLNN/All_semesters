SELECT AVG(Цена) AS Средняя_цена FROM Меню;
SELECT SUM(Цена) AS Цена_всего_меню FROM Меню;
SELECT MAX(Цена) AS Максимальная_цена_позиции FROM Меню;
SELECT MIN(Цена) AS Минимальная_цена_позиции FROM Меню;
SELECT Count(Цена) AS Позиций_в_меню FROM Меню;

SELECT Тип_продукта, COUNT(*) AS КоличествоТиповПродукта
FROM Поставщик
GROUP BY Тип_продукта;

SELECT Название, Цена
FROM Меню
ORDER BY Цена ASC;

SELECT Имя
FROM Сотрудник
WHERE Имя LIKE '';

SELECT Отчество
FROM Сотрудник
WHERE Отчество LIKE 'Павло___';
