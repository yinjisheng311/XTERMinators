CREATE DATABASE Xterminators CHARACTER SET UTF8;

CREATE USER XterminatorsUser@localhost IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON Xterminators.* TO XterminatorsUser@localhost;

FLUSH PRIVILEGES;

