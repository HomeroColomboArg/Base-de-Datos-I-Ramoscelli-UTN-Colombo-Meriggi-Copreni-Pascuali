
-- 9) Modificar el trigger

DELIMITER $$


DROP TRIGGER IF EXISTS trg_actualiza_saldo $$


CREATE TRIGGER trg_actualiza_saldo
AFTER INSERT ON Movimientos
FOR EACH ROW
BEGIN
  DECLARE v_saldo_anterior DECIMAL(10,2);

  
  SELECT saldo INTO v_saldo_anterior
  FROM Cuentas
  WHERE numero_cuenta = NEW.numero_cuenta;

  
  IF UPPER(NEW.tipo) = 'CREDITO' THEN
    UPDATE Cuentas
      SET saldo = saldo + NEW.importe
    WHERE numero_cuenta = NEW.numero_cuenta;
  ELSE
    UPDATE Cuentas
      SET saldo = saldo - NEW.importe
    WHERE numero_cuenta = NEW.numero_cuenta;
  END IF;

 
  INSERT INTO Historial_movimientos
    (id, numero_cuenta, numero_movimiento, saldo_anterior, saldo_actual)
  VALUES
    (
      (SELECT IFNULL(MAX(id), 0) + 1 FROM Historial_movimientos),
      NEW.numero_cuenta,
      NEW.numero_movimiento,
      v_saldo_anterior,
      (SELECT saldo FROM Cuentas WHERE numero_cuenta = NEW.numero_cuenta)
    );
END $$
DELIMITER ;
