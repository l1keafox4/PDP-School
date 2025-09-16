CREATE TABLE Avtomobillar (
    id SERIAL PRIMARY KEY,
    nomi VARCHAR(100),
    rangi VARCHAR(50),
    yili INTEGER,
    narxi NUMERIC(10, 2)
);

-- Mahsulot jadvalini yaratish
CREATE TABLE Mahsulot (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    narx NUMERIC(10, 2),
    mijoz_id INTEGER
);

-- Maktab jadvalini yaratish
CREATE TABLE Maktab (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(100),
    xodim INTEGER,
    talaba INTEGER
);