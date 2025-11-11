-- 4. Procedimiento: CuentasConSaldoMayorQue(límite)
DELIMITER $$
DROP PROCEDURE IF EXISTS CuentasConSaldoMayorQue $$
CREATE PROCEDURE CuentasConSaldoMayorQue(IN limite DECIMAL(10,2))
BEGIN
  SELECT numero_cuenta, saldo
  FROM Cuentas
  WHERE saldo > limite
  ORDER BY saldo DESC;
END $$
DELIMITER ;