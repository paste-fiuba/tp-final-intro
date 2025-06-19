CREATE DATABASE Ludoteca;

use Ludoteca;

CREATE TABLE Usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Productos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria ENUM('Juego de mesa', 'Juego de Cartas', 'Juego de rol', 'Otro') NOT NULL DEFAULT 'Otro',
    imagen LONGBLOB
);

CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE PedidoDetalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);


INSERT INTO Productos (nombre, descripcion, precio, stock, categoria)
VALUES
('Uno', 'El objetivo es ser el primero en quedarse sin cartas en la mano. Cada jugador debe ir descartando cartas que coincidan en color o número con la carta en juego. Además, hay cartas especiales que cambian el sentido del juego, hacen robar cartas o saltan turnos. Cuando a un jugador le queda una sola carta, debe decir “¡UNO!” o puede ser penalizado.', 10000, 20, 'Juego de Cartas'),

('Jenga', 'Jenga es un juego de habilidad física que consiste en retirar bloques de madera de una torre construida con 54 bloques, intentando no derribarla.', 10000, 15, 'Juego de mesa'),

('Ajedrez', 'El ajedrez es un juego de estrategia para dos personas que se juega sobre un tablero de 64 casillas, alternadas en colores claros y oscuros. Cada jugador comienza con 16 piezas: un rey, una dama (o reina), dos torres, dos alfiles, dos caballos y ocho peones. El objetivo del juego es dar jaque mate al rey del oponente, lo que significa dejarlo sin posibilidad de escapar a una amenaza de captura.', 15000, 10, 'Juego de mesa'),

('Dos', 'El objetivo es ser el primero en quedarse sin cartas en la mano. Cada jugador debe ir descartando cartas que coincidan en color o número con la carta en juego. Además, hay cartas especiales que cambian el sentido del juego, hacen robar cartas o saltan turnos. Cuando a un jugador le queda una sola carta, debe decir “¡DOS!” o puede ser penalizado.', 10000, 18, 'Juego de Cartas'),

('T.E.G.', 'El plan táctico y estratégico de guerra servirá para lograr un objetivo en un planisferio dividido en 50 países donde 6 ejércitos compiten por conquistar el mundo.', 50000, 8, 'Juego de mesa'),

('Monopoly', 'Monopoly es un juego de mesa basado en el intercambio y la compraventa de propiedades inmobiliarias. Los jugadores se mueven por un tablero, comprando propiedades, construyendo casas y hoteles, y cobrando alquileres a los demás jugadores.', 60000, 12, 'Juego de mesa'),

('Rompecabezas', 'Rompecabezas de animales, paisajes y más. 24 piezas de madera con ilustraciones coloridas. Ideal para niños de 3 a 6 años.', 20000, 25, 'Juego de mesa'),

('Ludo', 'Ludo es un juego de mesa clásico que se juega con fichas y un dado. El objetivo es llevar todas las fichas al centro del tablero antes que los demás jugadores. Es un juego de estrategia y suerte, ideal para toda la familia.', 25000, 14, 'Juego de mesa'),

('Clue', 'Clue es un juego de mesa de misterio y deducción. Los jugadores deben resolver un asesinato descubriendo quién es el asesino, con qué arma y en qué habitación ocurrió el crimen.', 60000, 7, 'Juego de mesa');

INSERT INTO Productos (nombre, descripcion, precio, stock, categoria)
VALUES
('Dungeons & Dragons', 'Dungeons & Dragons es un juego de rol de fantasía donde los jugadores crean personajes y participan en aventuras guiadas por un Dungeon Master. Es un juego de imaginación, estrategia y colaboración.', 80000, 5, 'Juego de rol')