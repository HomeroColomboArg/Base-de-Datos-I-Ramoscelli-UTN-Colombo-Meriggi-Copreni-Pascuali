-- 10 . Procedimiento con cursor: TotalMovimientosDelMes_Cursor
DELIMITER $$
DROP TRIGGER IF EXISTS trg_actualiza_saldo $$
CREATE TRIGGER trg_actualiza_saldo
AFTER INSERT ON Movimientos
FOR EACH ROW
BEGIN
  
  UPDATE Cuentas
  SET saldo = saldo + IF(UPPER(NEW.tipo) = 'CREDITO', NEW.importe, -NEW.importe)
  WHERE numero_cuenta = NEW.numero_cuenta;

 
  INSERT INTO Historial_movimientos (id, numero_cuenta, numero_movimiento, saldo_anterior, saldo_actual)
  SELECT
    (SELECT IFNULL(MAX(h.id), 0) + 1 FROM Historial_movimientos h),
    c.numero_cuenta,
    NEW.numero_movimiento,
    c.saldo - IF(UPPER(NEW.tipo) = 'CREDITO', NEW.importe, -NEW.importe) AS saldo_anterior,
    c.saldo AS saldo_actual
  FROM Cuentas c
  WHERE c.numero_cuenta = NEW.numero_cuenta;
END $$
DELIMITER ;
