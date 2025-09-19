<?php
// Простой тестовый скрипт для проверки работы PHP
echo "<h1>PHP работает</h1>";
echo "<p>Время сервера: " . date('Y-m-d H:i:s') . "</p>";
echo "<p>PHP версия: " . phpversion() . "</p>";

// Проверка соединения с базой данных
include 'admin/db_config.php';

echo "<h2>Проверка соединения с базой данных:</h2>";
if ($conn->connect_error) {
    echo "<p style='color: red;'>Ошибка соединения: " . $conn->connect_error . "</p>";
} else {
    echo "<p style='color: green;'>Соединение с базой данных успешно установлено</p>";
    
    // Проверка существования таблиц
    $tables = [
        'litebans_proof' => $conn->query("SHOW TABLES LIKE 'litebans_proof'")->num_rows > 0,
        'litebans_mute_proof' => $conn->query("SHOW TABLES LIKE 'litebans_mute_proof'")->num_rows > 0
    ];
    
    echo "<h3>Проверка существования таблиц:</h3>";
    echo "<ul>";
    foreach ($tables as $table => $exists) {
        echo "<li>" . $table . ": " . ($exists ? "<span style='color:green'>Существует</span>" : "<span style='color:red'>Не существует</span>") . "</li>";
    }
    echo "</ul>";
    
    // Проверка прав доступа к директории uploads
    echo "<h3>Проверка директории uploads:</h3>";
    $uploadsDir = dirname(__FILE__) . "/uploads/proofs/";
    echo "<p>Путь: " . $uploadsDir . "</p>";
    echo "<p>Существует: " . (file_exists($uploadsDir) ? "Да" : "Нет") . "</p>";
    echo "<p>Доступ на запись: " . (is_writable($uploadsDir) ? "Да" : "Нет") . "</p>";
    
    // Проверим содержимое директории
    echo "<h3>Содержимое директории uploads/proofs:</h3>";
    if (file_exists($uploadsDir)) {
        $files = scandir($uploadsDir);
        echo "<ul>";
        foreach ($files as $file) {
            if ($file != "." && $file != "..") {
                echo "<li>" . $file . " (" . filesize($uploadsDir . $file) . " байт)</li>";
            }
        }
        echo "</ul>";
    } else {
        echo "<p>Директория не существует</p>";
    }
}
?>
