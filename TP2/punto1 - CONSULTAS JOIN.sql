-- ¿Qué socios tienen barcos amarrados en un número de amarre mayor que 10?
SELECT DISTINCT s.nombre
FROM Socios s
JOIN Barcos b ON s.id_socio = b.id_socio
WHERE b.numero_amarre > 10;
-- ¿Cuáles son los nombres de los barcos y sus cuotas de aquellos barcos cuyo socio se llama 'Juan Pérez'?
SELECT b.nombre AS barco, b.cuota
FROM Barcos b
JOIN Socios s ON b.id_socio = s.id_socio
WHERE s.nombre = 'Juan Pérez';
-- ¿Cuántas salidas ha realizado el barco con matrícula 'ABC123'?
SELECT COUNT(sal.id_salida) AS cantidad_salidas
FROM Barcos b
JOIN Salidas sal ON b.matricula = sal.matricula
WHERE b.matricula = 'ABC123';
-- Lista los barcos que tienen una cuota mayor a 500 y sus respectivos socios.
SELECT b.nombre AS barco, s.nombre AS socio
FROM Barcos b
JOIN Socios s ON b.id_socio = s.id_socio
WHERE b.cuota > 500;
-- ¿Qué barcos han salido con destino a 'Mallorca'?
SELECT DISTINCT b.nombre AS barco
FROM Barcos b
JOIN Salidas s ON b.matricula = s.matricula
WHERE s.destino = 'Mallorca';
-- ¿Qué patrones (nombre y dirección) han llevado un barco cuyo socio vive en 'Barcelona'?
SELECT DISTINCT sal.patron_nombre, sal.patron_direccion
FROM Salidas sal
JOIN Barcos b ON sal.matricula = b.matricula
JOIN Socios s ON b.id_socio = s.id_socio
WHERE s.direccion LIKE '%Barcelona%';
