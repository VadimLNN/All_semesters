SELECT AVG(����) AS �������_���� FROM ����;
SELECT SUM(����) AS ����_�����_���� FROM ����;
SELECT MAX(����) AS ������������_����_������� FROM ����;
SELECT MIN(����) AS �����������_����_������� FROM ����;
SELECT Count(����) AS �������_�_���� FROM ����;

SELECT ���_��������, COUNT(*) AS �����������������������
FROM ���������
GROUP BY ���_��������;

SELECT ��������, ����
FROM ����
ORDER BY ���� ASC;

SELECT ���
FROM ���������
WHERE ��� LIKE '';

SELECT ��������
FROM ���������
WHERE �������� LIKE '�����___';
