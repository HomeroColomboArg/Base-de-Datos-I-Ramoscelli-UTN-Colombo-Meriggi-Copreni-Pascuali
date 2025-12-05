-- CREACIÓN DE BASE DE DATOS
CREATE DATABASE IF NOT EXISTS biblioteca_db;

USE biblioteca_db;

DROP TABLE IF EXISTS prestamos;
DROP TABLE IF EXISTS pagos;
DROP TABLE IF EXISTS libros;
DROP TABLE IF EXISTS usuarios;

-- TABLA USUARIOS

CREATE TABLE usuarios (
    id_usuario      INT UNSIGNED AUTO_INCREMENT,
    nombre          VARCHAR(50)      NOT NULL,
    apellido        VARCHAR(50)      NOT NULL,
    dni             VARCHAR(15)      NOT NULL,
    email           VARCHAR(100)     NOT NULL,
    telefono        VARCHAR(30),
    fecha_alta      DATE             NOT NULL,
    activo          TINYINT(1)       NOT NULL DEFAULT 1,
    CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuarios_dni   UNIQUE (dni),
    CONSTRAINT uq_usuarios_email UNIQUE (email)
);

-- TABLA LIBROS

CREATE TABLE libros (
    id_libro         INT UNSIGNED AUTO_INCREMENT,
    titulo           VARCHAR(150) NOT NULL,
    autor            VARCHAR(100) NOT NULL,
    anio_publicacion INT,
    isbn             VARCHAR(20),
    editorial        VARCHAR(100),
    categoria        VARCHAR(50),
    activo           TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT pk_libros PRIMARY KEY (id_libro),
    CONSTRAINT uq_libros_isbn UNIQUE (isbn)
);


-- indice para acelerar búsquedas por título/autor
CREATE INDEX idx_libros_titulo_autor
    ON libros (titulo, autor);

-- TABLA PAGOS
CREATE TABLE pagos (
    id_pago             INT UNSIGNED AUTO_INCREMENT,
    id_usuario          INT UNSIGNED      NOT NULL,
    anio                INT               NOT NULL,
    mes                 TINYINT UNSIGNED  NOT NULL,   -- 1 a 12
    fecha_vencimiento   DATE              NOT NULL,
    fecha_pago          DATE,
    monto               DECIMAL(10,2)     NOT NULL,
    pagado              TINYINT(1)        NOT NULL DEFAULT 0,  -- 0 = no pagado, 1 = pagado
    CONSTRAINT pk_pagos PRIMARY KEY (id_pago),
    CONSTRAINT uq_pagos_usuario_periodo UNIQUE (id_usuario, anio, mes),
    CONSTRAINT fk_pagos_usuarios
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- TABLA PRESTAMOS
CREATE TABLE prestamos (
    id_prestamo        INT UNSIGNED AUTO_INCREMENT,
    id_usuario         INT UNSIGNED      NOT NULL,
    id_libro           INT UNSIGNED      NOT NULL,
    fecha_prestamo     DATE              NOT NULL,
    fecha_vencimiento  DATE              NOT NULL,
    fecha_devolucion   DATE,
    estado             ENUM('PRESTADO','DEVUELTO','ATRASADO')
                       NOT NULL DEFAULT 'PRESTADO',
    CONSTRAINT pk_prestamos PRIMARY KEY (id_prestamo),
    CONSTRAINT fk_prestamos_usuarios
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_prestamos_libros
        FOREIGN KEY (id_libro)
        REFERENCES libros (id_libro)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- INSERTS INICIALES

INSERT INTO usuarios (nombre, apellido, dni, email, telefono, fecha_alta, activo) VALUES
('Juan',   'Pérez',      '30111222', 'juan.perez@example.com',     '291-4000001', '2025-03-10', 1),
('María',  'Gómez',      '30222333', 'maria.gomez@example.com',    '291-4000002', '2025-03-28', 1),
('Lucas',  'Fernández',  '30333444', 'lucas.fernandez@example.com','291-4000003', '2025-04-05', 1),
('Ana',    'Martínez',   '30444555', 'ana.martinez@example.com',   '291-4000004', '2025-04-22', 1),
('Sofía',  'López',      '30555666', 'sofia.lopez@example.com',    '291-4000005', '2025-05-03', 1),
('Diego',  'Rodríguez',  '30666777', 'diego.rodriguez@example.com','291-4000006', '2025-05-18', 1),
('Carla',  'Sosa',       '30777888', 'carla.sosa@example.com',     '291-4000007', '2025-05-30', 1),
('Martín', 'Ruiz',       '30888999', 'martin.ruiz@example.com',    '291-4000008', '2025-06-12', 1),
('Laura',  'Castro',     '30999000', 'laura.castro@example.com',   '291-4000009', '2025-06-20', 1),
('Pablo',  'Domínguez',  '31100111', 'pablo.dominguez@example.com','291-4000010', '2025-06-28', 1);



INSERT INTO libros (titulo, autor, anio_publicacion, isbn, editorial, categoria) VALUES
('Cien años de soledad',        'Gabriel García Márquez', 1967, '9780307474728', 'Sudamericana', 'Novela'),
('El señor de los anillos',     'J. R. R. Tolkien',       1954, '9780261102385', 'Minotauro',    'Fantasía'),
('1984',                        'George Orwell',          1949, '9780451524935', 'Debolsillo',   'Distopía'),
('Crónica de una muerte anunciada','Gabriel García Márquez',1981,'9780307474729','Sudamericana','Novela'),
('El nombre del viento',        'Patrick Rothfuss',       2007, '9788401352836', 'Plaza & Janés','Fantasía'),
('Harry Potter y la piedra filosofal','J. K. Rowling',    1997, '9788478884452', 'Salamandra',   'Fantasía'),
('Fahrenheit 451',              'Ray Bradbury',           1953, '9781451673319', 'Minotauro',    'Distopía'),
('El principito',               'Antoine de Saint-Exupéry',1943,'9780156012195','Emecé',        'Infantil'),
('La sombra del viento',        'Carlos Ruiz Zafón',      2001, '9788408172178', 'Planeta',     'Novela'),
('Rayuela',                     'Julio Cortázar',         1963, '9788426406066', 'Alfaguara',   'Novela');


INSERT INTO pagos (id_usuario, anio, mes, fecha_vencimiento, fecha_pago, monto, pagado) VALUES
(1, 2024, 10, '2024-10-10', '2024-10-09', 2500.00, 1), -- pagado
(1, 2024, 11, '2024-11-10', NULL,         2500.00, 0), -- moroso
(2, 2024, 10, '2024-10-10', '2024-10-15', 2500.00, 1),
(3, 2024, 10, '2024-10-10', NULL,         2500.00, 0),
(4, 2024, 10, '2024-10-10', '2024-10-08', 2500.00, 1),
(5, 2024, 10, '2024-10-10', NULL,         2500.00, 0),
(6, 2024, 10, '2024-10-10', '2024-10-11', 2500.00, 1),
(7, 2024, 10, '2024-10-10', NULL,         2500.00, 0);

INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_vencimiento, fecha_devolucion, estado) VALUES
(1, 1, '2024-10-01', '2024-10-15', '2024-10-14', 'DEVUELTO'),  -- sin atraso
(2, 2, '2024-10-05', '2024-10-20', '2024-10-25', 'DEVUELTO'),  -- con atraso
(3, 3, '2024-10-10', '2024-10-25', NULL,          'PRESTADO'), -- aún prestado
(1, 4, '2024-11-01', '2024-11-15', NULL,          'ATRASADO'); -- prestamo atrasado
