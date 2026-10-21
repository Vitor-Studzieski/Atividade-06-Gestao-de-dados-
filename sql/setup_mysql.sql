CREATE DATABASE IF NOT EXISTS `gestaodados`;
USE `gestaodados`;

CREATE TABLE IF NOT EXISTS `usuarios_temporarios` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nome_completo` VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS `usuarios_final` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `primeiro_nome` VARCHAR(50),
    `sobrenome` VARCHAR(100)
);

INSERT INTO `usuarios_temporarios` (`nome_completo`) VALUES
    ('Ewerton Silva'), ('Ana Paula Oliveira'), ('João Pedro Santos'), ('Maria Eduarda Costa'),
    ('Carlos Henrique Ferreira'), ('Beatriz Souza'), ('Lucas Gabriel Rodrigues'), ('Fernanda Lima'),
    ('Ricardo Alves'), ('Juliana Pereira'), ('Gabriel Nascimento'), ('Mariana Guimarães'),
    ('Thiago Mendes'), ('Camila Rocha'), ('Bruno Cardoso'), ('Larissa Freitas'),
    ('Marcelo Vieira'), ('Amanda Machado'), ('Felipe Castro'), ('Letícia Barbosa'),
    ('Diego Ribeiro'), ('Patrícia Gomes'), ('Rodrigo Carvalho'), ('Tatiana Martins'),
    ('Gustavo Araújo'), ('Priscila Melo'), ('André Luiz Moreira'), ('Vanessa Caldeira'),
    ('Marcos Vinícius Cunha'), ('Renata Lopes'), ('Alexandre Ramos'), ('Simone Teixeira'),
    ('Daniel Cavalcanti'), ('Aline Borges'), ('Eduardo Farias'), ('Cláudia Neves'),
    ('Leonardo Pires'), ('Suelen Viana'), ('Vitor Hugo Amaral'), ('Gisele Monteiro'),
    ('Caio Augusto Aguiar'), ('Bianca Peixoto'), ('Samuel Telles'), ('Karina Rezende'),
    ('Henrique Silveira'), ('Débora Porto'), ('Otávio Mesquita'), ('Lorena Caldas'),
    ('Hugo Magalhães'), ('Cintia Veras');
