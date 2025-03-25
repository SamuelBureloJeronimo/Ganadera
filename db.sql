CREATE DATABASE ganaderia_db;
USE ganaderia_db;

-- Tabla de Animales
CREATE TABLE animales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_arete VARCHAR(50) UNIQUE NOT NULL,
    especie VARCHAR(50),
    raza VARCHAR(50),
    peso DOUBLE,
    fecha_nacimiento DATE,
    estado ENUM('Disponible', 'Vendido', 'Enfermo', 'Muerto') DEFAULT 'Disponible'
);

-- Tabla de Ventas
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_animal INT,
    comprador VARCHAR(100),
    fecha_venta DATE,
    peso_kg DOUBLE,
    precio_kg DOUBLE,
    total DOUBLE GENERATED ALWAYS AS (peso_kg * precio_kg) STORED,
    observaciones TEXT,
    FOREIGN KEY (id_animal) REFERENCES animales(id) ON DELETE SET NULL
);

-- Tabla de Compras de Insumos
CREATE TABLE compras_insumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(255),
    cantidad DOUBLE,
    unidad VARCHAR(50), -- Kg, Litros, etc.
    precio_unitario DOUBLE,
    total DOUBLE GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    fecha_compra DATE,
    proveedor VARCHAR(255)
);

-- Tabla de Consumo de Insumos (Ej: alimento ganado)
CREATE TABLE consumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_animal INT,
    id_insumo INT,
    cantidad_usada DOUBLE,
    fecha DATE,
    observaciones TEXT,
    FOREIGN KEY (id_animal) REFERENCES animales(id) ON DELETE SET NULL,
    FOREIGN KEY (id_insumo) REFERENCES compras_insumos(id) ON DELETE SET NULL
);

-- Tabla de Finanzas (Ingresos y Egresos)
CREATE TABLE finanzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('Ingreso', 'Egreso') NOT NULL,
    descripcion TEXT,
    monto DOUBLE NOT NULL,
    fecha DATE NOT NULL
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Usuario') DEFAULT 'Usuario'
);
