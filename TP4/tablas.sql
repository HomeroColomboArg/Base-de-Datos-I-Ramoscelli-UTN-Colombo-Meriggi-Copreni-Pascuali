CREATE TABLE Clientes (
  numero_cliente INT PRIMARY KEY,
  dni INT NOT NULL UNIQUE,
  apellido VARCHAR(100) NOT NULL,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Cuentas (
  numero_cuenta INT PRIMARY KEY,
  numero_cliente INT NOT NULL,
  saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  FOREIGN KEY (numero_cliente) REFERENCES Clientes(numero_cliente)
);

CREATE TABLE Movimientos (
  numero_movimiento INT AUTO_INCREMENT PRIMARY KEY,
  numero_cuenta INT NOT NULL,
  fecha DATE NOT NULL,
  tipo ENUM('CREDITO','DEBITO') NOT NULL,
  importe DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (numero_cuenta) REFERENCES Cuentas(numero_cuenta)
);

CREATE TABLE Historial_movimientos (
  id INT PRIMARY KEY,
  numero_cuenta INT NOT NULL,
  numero_movimiento INT NOT NULL,
  saldo_anterior DECIMAL(10,2),
  saldo_actual DECIMAL(10,2),
  FOREIGN KEY (numero_cuenta) REFERENCES Cuentas(numero_cuenta)
);