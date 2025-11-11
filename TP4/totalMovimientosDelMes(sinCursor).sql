-- 5. Procedimiento: TotalMovimientosDelMes (sin cursor)
DELIMITER $$
DROP PROCEDURE IF EXISTS TotalMovimientosDelMes $$
CREATE PROCEDURE TotalMovimientosDelMes(IN p_cuenta INT, OUT p_total DECIMAL(10,2))
BEGIN
  SELECT COALESCE(SUM(CASE WHEN tipo='CREDITO' THEN importe ELSE -importe END), 0)
    INTO p_total
  FROM Movimientos
  WHERE numero_cuenta = p_cuenta
    AND MONTH(fecha) = MONTH(CURDATE())
    AND YEAR(fecha) = YEAR(CURDATE());
END $$
DELIMITER ;