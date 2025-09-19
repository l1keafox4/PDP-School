<?php
/**
 * Скрипт для настройки таблицы нарушений хелперов
 */

// Включаем вывод ошибок для отладки
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Подключение к базе данных
require_once __DIR__ . '/db_config.php';

if (!$conn) {
    die("Ошибка: Не удалось подключиться к базе данных");
}

echo "Создание или обновление таблицы для отслеживания нарушений хелперов...<br>";

// Создаем таблицу для отслеживания нарушений, если её нет
try {
    $conn->query("
        CREATE TABLE IF NOT EXISTS litebans_helper_violations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            helper_name VARCHAR(255) NOT NULL,
            ban_id INT NOT NULL,
            player_name VARCHAR(255) NOT NULL,
            violation_time INT NOT NULL,
            processed TINYINT(1) DEFAULT 0
        )
    ");
    
    echo "Таблица litebans_helper_violations успешно создана или уже существует<br>";
    
    // Создание индекса для ускорения запросов по имени хелпера
    $conn->query("
        CREATE INDEX IF NOT EXISTS idx_helper_name ON litebans_helper_violations (helper_name)
    ");
    
    echo "Индекс для поля helper_name успешно создан<br>";
    
    echo "<h3>Установка системы нарушений хелперов завершена успешно!</h3>";
} catch (Exception $e) {
    echo "Ошибка при создании таблицы: " . $e->getMessage();
}
?>
