<?php
/**
 * Тестовый скрипт для проверки отправки уведомлений в Telegram
 */

// Включаем вывод ошибок для отладки
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Настройки Telegram
$telegram_bot_token = '7665890197:AAE89GCrTvoL1C_F0HLNJpItW--crlrt91A';
$telegram_chat_id = '1400003638';

// Функция для отправки сообщения в Telegram
function send_telegram_message($message) {
    global $telegram_bot_token, $telegram_chat_id;
    
    echo "Отправка сообщения в Telegram...<br>";
    
    $url = "https://api.telegram.org/bot$telegram_bot_token/sendMessage";
    $params = [
        'chat_id' => $telegram_chat_id,
        'text' => $message,
        'parse_mode' => 'HTML'
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        echo "Ошибка отправки сообщения: $error<br>";
        return false;
    }
    
    if ($http_code >= 200 && $http_code < 300) {
        echo "Сообщение успешно отправлено (HTTP код: $http_code)<br>";
        echo "Ответ API: <pre>" . htmlspecialchars($response) . "</pre>";
        return true;
    } else {
        echo "Ошибка отправки сообщения. HTTP код: $http_code<br>";
        echo "Ответ API: <pre>" . htmlspecialchars($response) . "</pre>";
        return false;
    }
}

// Тестовое сообщение
$message = "<b>🔵 ТЕСТОВОЕ СООБЩЕНИЕ</b>\n\nЭто тестовое сообщение для проверки работы уведомлений. Если вы видите это сообщение, значит система работает корректно.";

// Отправляем тестовое сообщение
send_telegram_message($message);

echo "<p>Тест завершен. Проверьте свой Telegram, должно прийти сообщение.</p>";
?>
