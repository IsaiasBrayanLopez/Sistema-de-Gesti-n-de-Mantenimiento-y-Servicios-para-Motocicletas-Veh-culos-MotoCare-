-- Script de creacion de base de datos y tablas para MotoCare API
CREATE DATABASE IF NOT EXISTS motocare_db;
USE motocare_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de registros de servicio
CREATE TABLE IF NOT EXISTS registros_servicio (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_servicio VARCHAR(80) NOT NULL,
    kilometraje INT NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    fecha_servicio DATE NOT NULL,
    proximo_kilometraje INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    observaciones TEXT,
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Datos semilla iniciales
INSERT INTO usuarios (nombre, email, password_hash)
SELECT 'Usuario Prueba', 'demo@motocare.com', '123456'
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'demo@motocare.com');

INSERT INTO registros_servicio
(id_usuario, tipo_servicio, kilometraje, costo, fecha_servicio, proximo_kilometraje, estado, observaciones)
SELECT 1, 'Cambio de aceite', 12000, 450.00, '2026-11-20', 15000, 'Completado', 'Aceite sintetico 10W-40'
WHERE NOT EXISTS (SELECT 1 FROM registros_servicio WHERE id_usuario = 1 AND tipo_servicio = 'Cambio de aceite');

INSERT INTO registros_servicio
(id_usuario, tipo_servicio, kilometraje, costo, fecha_servicio, proximo_kilometraje, estado, observaciones)
SELECT 1, 'Ajuste de frenos', 12500, 280.00, '2026-11-26', 17500, 'Pendiente', 'Revision de balatas delanteras'
WHERE NOT EXISTS (SELECT 1 FROM registros_servicio WHERE id_usuario = 1 AND tipo_servicio = 'Ajuste de frenos');
