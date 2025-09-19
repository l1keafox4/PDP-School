<?php
session_start();

// Очистка всех переменных сессии
$_SESSION = array();

// Уничтожение сессии
session_destroy();

// Перенаправление на страницу входа
header("Location: login.php");
exit;
?>
