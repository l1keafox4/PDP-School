<?php
// Параметры подключения к базе данных
$host = "37.27.49.26:3306";
$username = "litebans";
$password = "your_password"; // Замените на ваш пароль
$database = "litebans";

// Создание соединения
$conn = new mysqli($host, $username, $password, $database);

// Проверка соединения
if ($conn->connect_error) {
    die("Ошибка подключения: " . $conn->connect_error);
}

// Установка кодировки
$conn->set_charset("utf8mb4");
?>
