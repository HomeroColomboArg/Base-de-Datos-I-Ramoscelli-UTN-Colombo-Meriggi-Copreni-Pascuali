-- 7. Procedmiento: Extraer(cuenta, monto)
DELIMITER $$
DROP PROCEDURE IF EXISTS Extraer $$
CREATE PROCEDURE Extraer(IN p_cuenta INT, IN p_monto DECIMAL(10,2))
BEGIN
  DECLARE v_saldo DECIMAL(10,2);

  SELECT saldo INTO v_saldo
  FROM Cuentas
  WHERE numero_cuenta = p_cuenta
  FOR UPDATE;

  IF v_saldo IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta inexstente';
  END IF;

  IF v_saldo < p_monto THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Fondos insuficientes';
  END IF;

  INSERT INTO Movimientos (numero_cuenta, fecha, tipo, importe)
  VALUES (p_cuenta, CURDATE(), 'DEBITO', p_monto);
END $$
DELIMITER ;