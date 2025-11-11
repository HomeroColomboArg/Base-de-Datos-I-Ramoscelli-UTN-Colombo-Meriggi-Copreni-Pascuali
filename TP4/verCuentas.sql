-- 3. Procedimiento: VerCuentas()
DELIMITER $$
DROP PROCEDURE IF EXISTS VerCuentas $$
CREATE PROCEDURE VerCuentas()
BEGIN
  SELECT c.numero_cuenta, CONCAT(cl.apellido, ', ', cl.nombre) AS cliente, c.saldo
  FROM Cuentas c
  JOIN Clientes cl ON cl.numero_cliente = c.numero_cliente
  ORDER BY c.numero_cuenta;
END $$
DELIMITER ;