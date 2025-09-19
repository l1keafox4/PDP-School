
<?php
/**
 * Скрипт для автоматического разбана игроков, если хелпер не предоставил пруф в течение 2 часов
 * Отслеживает нарушения хелперов и отправляет уведомления в Telegram
 * Запускать этот скрипт через cron каждые 5-10 минут
 */

// Включаем вывод ошибок для отладки
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Настройка пути к лог-файлу
$log_file = __DIR__ . '/../PLUGIN_DEVELOPING/auto_unban_log.txt';

// Настройки Telegram
$telegram_bot_token = '7665890197:AAE89GCrTvoL1C_F0HLNJpItW--crlrt91A';
$telegram_chat_id = '1400003638';

// Настройки API Pterodactyl
$pterodactyl_api_key = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV';
$pterodactyl_server_url = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command';

// Функция для логирования
function log_message($message) {
    global $log_file;
    $timestamp = date('[Y-m-d H:i:s]');
    file_put_contents($log_file, "$timestamp $message\n", FILE_APPEND);
}

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
    
    log_message("Сообщение успешно отправлено в Telegram");
    return true;
}

// Функция для выполнения команды через API Pterodactyl
function execute_pterodactyl_command($command) {
    global $pterodactyl_api_key, $pterodactyl_server_url;
    
    $data = json_encode(['command' => $command]);
    
    $ch = curl_init($pterodactyl_server_url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Accept: Application/vnd.pterodactyl.v1+json',
        'Authorization: Bearer ' . $pterodactyl_api_key
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        log_message("Ошибка выполнения команды: $error");
        return false;
    }
    
    if ($http_code >= 200 && $http_code < 300) {
        log_message("Команда успешно выполнена: $command");
        return true;
    } else {
        log_message("Ошибка выполнения команды ($http_code): $command");
        return false;
    }
}

// Функция для регистрации нарушения хелпера
function register_helper_violation($helper_name, $ban_id, $player_name) {
    global $conn;
    
    try {
        // СНАЧАЛА ПРОВЕРЯЕМ НАЛИЧИЕ ПРУФА - ЭТО САМАЯ ВАЖНАЯ ПРОВЕРКА
        // Если есть пруф, никогда не регистрируем нарушение
        $proof_check = $conn->prepare("
            SELECT COUNT(*) as count 
            FROM litebans_ban_proofs 
            WHERE ban_id = ?
        ");
        $proof_check->bind_param("i", $ban_id);
        $proof_check->execute();
        $proof_result = $proof_check->get_result();
        $has_proof = $proof_result->fetch_assoc()['count'] > 0;
        
        if ($has_proof) {
            log_message("ЗАЩИТА ОТ ОШИБОК: Для бана ID: $ban_id уже добавлен пруф. Нарушение НЕ БУДЕТ зарегистрировано!");
            return 0; // Если есть пруф, возвращаем 0 нарушений
        }
        
        // Создаем таблицу для отслеживания нарушений, если её нет
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
        
        // Сначала проверяем, был ли уже зарегистрирован этот бан как нарушение
        $check_query = $conn->prepare("SELECT COUNT(*) as count FROM litebans_helper_violations WHERE ban_id = ?");
        $check_query->bind_param("i", $ban_id);
        $check_query->execute();
        $result = $check_query->get_result();
        $exists = $result->fetch_assoc()['count'] > 0;
        
        if ($exists) {
            log_message("Нарушение для бана ID: $ban_id уже было зарегистрировано ранее.");
            
            // Получаем количество нарушений
            $violations_query = $conn->prepare("SELECT COUNT(*) as count FROM litebans_helper_violations WHERE helper_name = ?");
            $violations_query->bind_param("s", $helper_name);
            $violations_query->execute();
            $result = $violations_query->get_result();
            return $result->fetch_assoc()['count'];
        }
        
        // ПОСЛЕДНЯЯ ПРОВЕРКА ПЕРЕД ДОБАВЛЕНИЕМ
        // Еще раз проверяем наличие пруфа для полной уверенности
        $proof_check->execute();
        $proof_result = $proof_check->get_result();
        $has_proof = $proof_result->fetch_assoc()['count'] > 0;
        
        if ($has_proof) {
            log_message("ПОСЛЕДНЯЯ ЗАЩИТА: Для бана ID: $ban_id был добавлен пруф. Нарушение не будет зарегистрировано.");
            return 0;
        }
        
        // Добавляем запись о нарушении
        $stmt = $conn->prepare("INSERT INTO litebans_helper_violations (helper_name, ban_id, player_name, violation_time) VALUES (?, ?, ?, ?)");
        $time = time();
        $stmt->bind_param("sisi", $helper_name, $ban_id, $player_name, $time);
        $stmt->execute();
        
        // Получаем количество нарушений этого хелпера
        $violations_query = $conn->prepare("SELECT COUNT(*) as count FROM litebans_helper_violations WHERE helper_name = ?");
        $violations_query->bind_param("s", $helper_name);
        $violations_query->execute();
        $result = $violations_query->get_result();
        $violations_count = $result->fetch_assoc()['count'];
        
        log_message("Зарегистрировано нарушение для хелпера $helper_name. Всего нарушений: $violations_count");
        
        return $violations_count;
    } catch (Exception $e) {
        log_message("Ошибка при регистрации нарушения: " . $e->getMessage());
        return false;
    }
}

// Функция для удаления хелпера после 5 нарушений
function punish_helper($helper_name) {
    global $conn;
    
    log_message("Применение санкций к хелперу $helper_name после 5 нарушений");
    
    try {
        // Очистка прав в игре
        $clear_command = "lp user $helper_name clear";
        execute_pterodactyl_command($clear_command);
        
        // Бан хелпера в игре
        $ban_command = "ban $helper_name prooflarni vaqtida saytga joylamagani uchun bo'shatilindi";
        execute_pterodactyl_command($ban_command);
        
        // Удаление хелпера из базы данных
        $delete_query = $conn->prepare("DELETE FROM litebans_users WHERE username = ? AND role = 'helper'");
        $delete_query->bind_param("s", $helper_name);
        $delete_query->execute();
        
        // Очистка счетчика нарушений для этого хелпера
        // Вместо обновления статуса, полностью удаляем все нарушения этого хелпера
        $delete_violations = $conn->prepare("DELETE FROM litebans_helper_violations WHERE helper_name = ?");
        $delete_violations->bind_param("s", $helper_name);
        $delete_violations->execute();
        
        log_message("Счетчик нарушений для хелпера $helper_name полностью очищен");
        
        // Отправка уведомления в Telegram
        $message = "<b>🔴 ХЕЛПЕР УДАЛЕН</b>\n\nХелпер <b>$helper_name</b> был удален из системы за неоднократное нарушение правил предоставления пруфов (5/5 нарушений)";
        send_telegram_message($message);
        
        log_message("Хелпер $helper_name успешно удален из системы");
        return true;
    } catch (Exception $e) {
        log_message("Ошибка при удалении хелпера: " . $e->getMessage());
        return false;
    }
}

// Начало выполнения скрипта
log_message("=== Запуск проверки банов без пруфов ===");

// Подключение к базе данных
require_once __DIR__ . '/db_config.php';

if (!$conn) {
    log_message("Ошибка: Не удалось подключиться к базе данных");
    exit;
}

// Получение списка хелперов из базы данных
try {
    log_message("Получение списка хелперов из базы данных");
    
    $helpers_query = "SELECT username FROM litebans_users WHERE role = 'helper'";
    $helpers_result = $conn->query($helpers_query);
    
    if (!$helpers_result) {
        throw new Exception("Ошибка выполнения запроса: " . $conn->error);
    }
    
    $helpers = [];
    while ($row = $helpers_result->fetch_assoc()) {
        $helpers[] = $row['username'];
    }
    
    $helpers_count = count($helpers);
    log_message("Получено $helpers_count хелперов из базы данных");
    
    if ($helpers_count === 0) {
        log_message("Предупреждение: Список хелперов пуст, проверка не будет выполнена");
        log_message("=== Завершение проверки ===\n");
        exit;
    }
} catch (Exception $e) {
    log_message("Ошибка при получении списка хелперов: " . $e->getMessage());
    log_message("=== Завершение проверки с ошибкой ===\n");
    exit;
}

// Преобразуем список хелперов в строку для SQL запроса
$helpers_list = "'" . implode("','", $helpers) . "'";

// Получаем текущее время в формате UNIX timestamp в миллисекундах (как в LiteBans)
$current_time = time() * 1000;

// Временная граница для проверки - 1 минута назад от текущего времени (фиксированное значение)
// Мы используем фиксированную проверку, а не относительно последнего запуска скрипта
$time_limit = $current_time - (120 * 60 * 1000); // 1 минута - ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!

// Сохраняем последнюю временную метку для отслеживания новых банов, но не для времени проверки
$timestamp_file = __DIR__ . '/../PLUGIN_DEVELOPING/last_unban_check.txt';
if (!file_exists($timestamp_file)) {
    // Устанавливаем начальную временную метку (текущее время минус 1 день)
    $initial_timestamp = $current_time - (24 * 60 * 60 * 1000); // 1 день назад
    file_put_contents($timestamp_file, $initial_timestamp);
    log_message("Создан файл временной метки. Будут обрабатываться только баны, созданные после " . date('Y-m-d H:i:s', $initial_timestamp/1000));
}

// Читаем последнюю временную метку только для новых банов
$last_check_timestamp = intval(file_get_contents($timestamp_file));
log_message("Последнее время проверки: " . date('Y-m-d H:i:s', $last_check_timestamp/1000));
log_message("Текущее время: " . date('Y-m-d H:i:s', time()));
log_message("Время проверки для разбана (current_time - 1 min): " . date('Y-m-d H:i:s', $time_limit/1000));

// SQL запрос для поиска банов без пруфов, наложенных хелперами
$query = "
    SELECT b.id, b.uuid, 
           h.name AS player_name,
           b.banned_by_name, 
           b.reason, 
           b.time,
           b.until
    FROM litebans_bans b
    LEFT JOIN litebans_history h ON b.uuid = h.uuid
    LEFT JOIN (
        SELECT DISTINCT ban_id FROM litebans_ban_proofs
    ) p ON b.id = p.ban_id
    WHERE 
        b.active = 1
        AND p.ban_id IS NULL  -- Проверка на отсутствие пруфа
        AND b.banned_by_name IN ($helpers_list)
        AND b.time > $last_check_timestamp
        AND b.time < $time_limit
    GROUP BY b.id
    ORDER BY b.time DESC
";

log_message("SQL запрос: $query");
log_message("Список хелперов: $helpers_list");

log_message("Выполнение SQL запроса для поиска банов без пруфов");

try {
    $result = $conn->query($query);
    
    if (!$result) {
        throw new Exception("Ошибка выполнения запроса: " . $conn->error);
    }
    
    $count = $result->num_rows;
    log_message("Найдено $count банов без пруфов, наложенных хелперами более 2 часов назад");
    
    if ($count === 0) {
        log_message("Нет банов для разбана");
        log_message("=== Завершение проверки ===\n");
        exit;
    }
    
    // Обрабатываем каждый бан
    while ($ban = $result->fetch_assoc()) {
        $player_name = $ban['player_name'];
        $helper_name = $ban['banned_by_name'];
        $ban_id = $ban['id'];
        $ban_time = date('Y-m-d H:i:s', intval($ban['time'] / 1000));
        
        log_message("Обработка бана ID: $ban_id, Игрок: $player_name, Забанен хелпером: $helper_name, Время бана: $ban_time");
        
        // Вместо регистрации нарушения хелпера сначала всегда проверяем наличие пруфа
        // Проверяем, не был ли добавлен пруф для этого бана
        $proof_check = $conn->prepare("SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = ?");
        $proof_check->bind_param("i", $ban_id);
        $proof_check->execute();
        $proof_result = $proof_check->get_result();
        $has_proof = $proof_result->fetch_assoc()['count'] > 0;
        
        if ($has_proof) {
            log_message("Для бана ID: $ban_id уже добавлен пруф. Пропускаем обработку.");
            continue; // Пропускаем этот бан и переходим к следующему
        }
        
        // Только если пруфа нет, регистрируем нарушение
        $violation_count = register_helper_violation($helper_name, $ban_id, $player_name);
        
        // Проверяем ещё раз, если нарушение было зарегистрировано
        if ($violation_count > 0) {
            // Ещё раз проверяем, не был ли опубликован пруф
            $proof_check = $conn->prepare("SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = ?");
            $proof_check->bind_param("i", $ban_id);
            $proof_check->execute();
            $proof_result = $proof_check->get_result();
            $has_proof = $proof_result->fetch_assoc()['count'] > 0;
            
            if ($has_proof) {
                log_message("Для бана ID: $ban_id обнаружен опубликованный пруф. Отмена обработки нарушения.");
                continue; // Пропускаем этот бан и переходим к следующему
            }
            
            // Отправляем уведомление в Telegram только если пруф действительно отсутствует
            $telegram_message = "<b>🔵 НАРУШЕНИЕ ПРАВИЛ</b>\n\nХелпер <b>$helper_name</b> не опубликовал пруф в течение 2 часов.\n\nИгрок: <b>$player_name</b>\nВремя бана: <b>$ban_time</b>\nСтатус: <b>$violation_count/5</b> предупреждений";
            send_telegram_message($telegram_message);
            
            // Проверка количества нарушений и применение наказания
            if ($violation_count >= 5) {
                log_message("Хелпер $helper_name получил 5 нарушений. Удаление из системы...");
                punish_helper($helper_name);
                continue; // После наказания переходим к следующему бану
            }
        } else {
            log_message("Нарушение не было зарегистрировано для бана ID: $ban_id (возможно, пруф уже был добавлен)");
            continue; // Если нарушение не было зарегистрировано, пропускаем этот бан
        }
        
        // Формирование команды разбана
        $unban_reason = "Proof yo'q";
        $command = "unban $player_name $unban_reason";
        
        log_message("Отправка команды разбана: $command");
        
        // Выполнение команды разбана
        $success = execute_pterodactyl_command($command);
        
        if ($success) {
            // Обновляем статус бана в базе данных - деактивируем его
            try {
                // Проверяем формат даты в базе данных
                $date_format_query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'litebans' AND TABLE_NAME = 'litebans_bans' AND COLUMN_NAME = 'removed_by_date'";
                $date_format_result = $conn->query($date_format_query);
                $date_format = $date_format_result->fetch_assoc()['DATA_TYPE'];
                
                log_message("Тип данных поля removed_by_date: $date_format");
                
                // Используем правильный формат даты в зависимости от типа поля
                if ($date_format == 'timestamp' || $date_format == 'datetime') {
                    // Если поле типа timestamp или datetime, преобразуем из миллисекунд в секунды
                    $removed_date = date('Y-m-d H:i:s', intval($current_time / 1000));
                    $update_query = "UPDATE litebans_bans SET active = 0, removed_by_name = 'AutoUnban', removed_by_date = '$removed_date', removed_by_reason = 'Proof yo`q' WHERE id = $ban_id";
                } else {
                    // По умолчанию используем миллисекунды как было раньше
                    $update_query = "UPDATE litebans_bans SET active = 0, removed_by_name = 'AutoUnban', removed_by_date = $current_time, removed_by_reason = 'Proof yo`q' WHERE id = $ban_id";
                }
                
                log_message("SQL запрос обновления: $update_query");
                $conn->query($update_query);
                
                if ($conn->affected_rows > 0) {
                    log_message("Бан с ID $ban_id деактивирован в базе данных");
                } else {
                    log_message("Предупреждение: Не удалось деактивировать бан в базе данных");
                }
            } catch (Exception $e) {
                log_message("Ошибка при обновлении базы данных: " . $e->getMessage());
            }
            
            // Если это 5-е нарушение, применяем санкции к хелперу
            if ($violation_count >= 5) {
                punish_helper($helper_name);
            }
        }
        
        // Небольшая пауза между запросами, чтобы не перегружать API
        sleep(1);
    }
    
} catch (Exception $e) {
    log_message("Ошибка: " . $e->getMessage());
}

// Обновляем файл временной метки только если были обработаны баны
if (isset($count) && $count > 0) {
    file_put_contents($timestamp_file, $current_time);
    log_message("Временная метка обновлена после обработки $count банов");
}

log_message("=== Завершение проверки ===\n");
?>
