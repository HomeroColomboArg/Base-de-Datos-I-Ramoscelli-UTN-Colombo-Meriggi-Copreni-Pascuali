-- 10) Procedimiento con cursor: AplicarInteres

DELIMITER $$
DROP PROCEDURE IF EXISTS AplicarInteres $$
CREATE PROCEDURE AplicarInteres(IN p_porcentaje DECIMAL(5,2), IN p_min_saldo DECIMAL(10,2))
BEGIN
  DECLARE v_cuenta INT;
  DECLARE v_saldo DECIMAL(10,2);
  DECLARE fin INT DEFAULT 0;

  DECLARE cur CURSOR FOR
    SELECT numero_cuenta, saldo FROM Cuentas WHERE saldo > p_min_saldo;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fin = 1;

  OPEN cur;
  bucle: LOOP
    FETCH cur INTO v_cuenta, v_saldo;
    IF fin = 1 THEN LEAVE bucle; END IF;

    INSERT INTO Movimientos (numero_cuenta, fecha, tipo, importe)
    VALUES (v_cuenta, CURDATE(), 'CREDITO', ROUND(v_saldo * (p_porcentaje/100), 2));
  END LOOP;
  CLOSE cur;
END $$
DELIMITER ;