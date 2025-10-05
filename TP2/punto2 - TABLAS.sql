CREATE TABLE Clientes (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(255)
);


CREATE TABLE Asuntos (
    numero_expediente INTEGER PRIMARY KEY,
    dni_cliente VARCHAR(20),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20),
    FOREIGN KEY (dni_cliente) REFERENCES Clientes(dni)
);


CREATE TABLE Procuradores (
    id_procurador INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(255)
);


CREATE TABLE Asuntos_Procuradores (
    numero_expediente INTEGER,
    id_procurador INTEGER,
    PRIMARY KEY (numero_expediente, id_procurador),
    FOREIGN KEY (numero_expediente) REFERENCES Asuntos(numero_expediente),
    FOREIGN KEY (id_procurador) REFERENCES Procuradores(id_procurador)
);
