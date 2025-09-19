<?php
/**
 * Скрипт для мониторинга новых банов и добавления пруфов
 * Запускать этот скрипт через cron каждые 5 минут
 */

// Включаем вывод ошибок для отладки
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Настройка пути к лог-файлу
$log_file = __DIR__ . '/../PLUGIN_DEVELOPING/ban_activity.log';

// Функция для логирования
function log_message($message) {
    global $log_file;
    $timestamp = date('[Y-m-d H:i:s]');
    file_put_contents($log_file, "$timestamp $message\n", FILE_APPEND);
}

// Подключение к базе данных
require_once __DIR__ . '/db_config.php';

if (!$conn) {
    log_message("Ошибка: Не удалось подключиться к базе данных");
    exit;
}

// Создаем таблицу для отслеживания обработанных банов, если её нет
$conn->query("
    CREATE TABLE IF NOT EXISTS litebans_ban_monitor (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ban_id INT NOT NULL UNIQUE,
        processed TINYINT(1) DEFAULT 0,
        proof_added TINYINT(1) DEFAULT 0,
        created_at INT NOT NULL
    )
");

// Создаем таблицу для хранения пруфов, если её нет
$conn->query("
    CREATE TABLE IF NOT EXISTS litebans_ban_proofs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ban_id INT NOT NULL,
        admin_name VARCHAR(255) NOT NULL,
        proof_link TEXT NOT NULL,
        time BIGINT NOT NULL,
        UNIQUE KEY (ban_id)
    )
");

// Настройки Telegram
$telegram_bot_token = '7665890197:AAE89GCrTvoL1C_F0HLNJpItW--crlrt91A';
$telegram_chat_id = '1400003638';

// Функция для отправки сообщения в Telegram
function send_telegram_message($message) {
    global $telegram_bot_token, $telegram_chat_id;
    
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
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        log_message("Ошибка отправки сообщения в Telegram: $error");
        return false;
    }
    
    return true;
}

// 1. Проверка новых банов
log_message("=== Начало проверки новых банов ===");

// Создаем файл временной метки, если его нет
$timestamp_file = __DIR__ . '/../PLUGIN_DEVELOPING/last_ban_check.txt';
if (!file_exists($timestamp_file)) {
    // Устанавливаем начальную временную метку (текущее время минус 1 день)
    $current_timestamp = time() * 1000 - (24 * 60 * 60 * 1000);
    file_put_contents($timestamp_file, $current_timestamp);
    log_message("Создан файл временной метки. Будут обрабатываться только баны, созданные после " . date('Y-m-d H:i:s', $current_timestamp/1000));
}

// НЕ ОБНОВЛЯТЬ временную метку при каждом запуске!
// Будем обновлять ее только при обнаружении новых банов
$last_check_timestamp = intval(file_get_contents($timestamp_file));
log_message("Последнее время проверки: " . date('Y-m-d H:i:s', $last_check_timestamp/1000));
log_message("Текущее время: " . date('Y-m-d H:i:s', time()));

// Ищем новые баны, которые были созданы после последней проверки
$new_bans_query = "
    SELECT 
        b.id, 
        b.uuid, 
        h.name AS player_name, 
        b.banned_by_uuid,
        b.banned_by_name AS admin_name, 
        b.reason, 
        b.time
    FROM litebans_bans b
    LEFT JOIN litebans_history h ON b.uuid = h.uuid
    WHERE 
        b.active = 1
        AND b.time > $last_check_timestamp
    ORDER BY b.time DESC
";

log_message("SQL запрос: $new_bans_query");

$new_bans_result = $conn->query($new_bans_query);

if (!$new_bans_result) {
    log_message("Ошибка выполнения запроса новых банов: " . $conn->error);
} else {
    $count = $new_bans_result->num_rows;
    log_message("Найдено $count новых банов");
    
    while ($ban = $new_bans_result->fetch_assoc()) {
        $ban_id = $ban['id'];
        $player_name = $ban['player_name'] ?: "Игрок с UUID " . $ban['uuid'];
        $admin_name = !empty($ban['admin_name']) ? $ban['admin_name'] : "Неизвестный админ";
        $reason = $ban['reason'] ?: "Не указана";
        $ban_time = intval($ban['time'] / 1000);
        $ban_date = date('Y-m-d H:i:s', $ban_time);
        
        // Вычисляем срок публикации пруфа (3 минуты от времени бана - ДЛЯ ТЕСТИРОВАНИЯ)
        // ОБЫЧНОЕ ЗНАЧЕНИЕ (раскомментировать после тестирования):
        // $proof_deadline = date('Y-m-d H:i:s', $ban_time + (2 * 60 * 60)); // 2 часа
        $proof_deadline = date('Y-m-d H:i:s', $ban_time + (3 * 60)); // 3 минуты - ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!
        
        // Проверяем, является ли админ хелпером
        $is_helper = false;
        $helper_check = $conn->prepare("SELECT COUNT(*) as count FROM litebans_users WHERE username = ? AND role = 'helper'");
        $helper_check->bind_param("s", $admin_name);
        $helper_check->execute();
        $helper_result = $helper_check->get_result();
        $is_helper = $helper_result->fetch_assoc()['count'] > 0;
        
        // Добавляем запись в лог и монитор-таблицу
        $insert = $conn->prepare("INSERT INTO litebans_ban_monitor (ban_id, processed, proof_added, created_at) VALUES (?, 1, 0, ?)");
        $current_time = time();
        $insert->bind_param("ii", $ban_id, $current_time);
        $insert->execute();
        
        // Формируем сообщение и отправляем в Telegram только если бан создан хелпером
        if ($is_helper) {
            $log_message = "Хелпер под ником $admin_name забанил игрока $player_name. Он должен опубликовать пруф до $proof_deadline";
            $telegram_message = "<b>🔵 НОВЫЙ БАН ОТ ХЕЛПЕРА</b>\n\nХелпер <b>$admin_name</b> забанил игрока <b>$player_name</b>.\n\nПричина: <code>$reason</code>\n\nПруф должен быть опубликован до: <b>$proof_deadline</b>";
            
            log_message($log_message);
            send_telegram_message($telegram_message);
        } else {
            // Для не-хелперов просто записываем в лог без отправки в Telegram
            $log_message = "Администратор $admin_name забанил игрока $player_name.";
            log_message($log_message);
        }
    }
    
    // Обновляем временную метку только если были найдены новые баны
    if ($count > 0) {
        file_put_contents($timestamp_file, time() * 1000);
    }
}

log_message("=== Завершение мониторинга банов ===\n");
?>
