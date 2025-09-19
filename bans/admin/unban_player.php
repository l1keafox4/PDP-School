<?php
// Включаем отображение всех ошибок
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Создаем лог-файл если не существует
$logFile = __DIR__ . '/../PLUGIN_DEVELOPING/unban_api.log';
$logDir = dirname($logFile);
if (!file_exists($logDir)) {
    mkdir($logDir, 0755, true);
}

// Пишем в лог начало выполнения скрипта
file_put_contents(
    $logFile, 
    date('[Y-m-d H:i:s] ') . "===== ЗАПУСК СКРИПТА РАЗБАНА =====\n" .
    "REQUEST_METHOD: " . $_SERVER['REQUEST_METHOD'] . "\n" .
    "POST данные: " . print_r($_POST, true) . "\n",
    FILE_APPEND
);

// Проверяем метод запроса
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    file_put_contents($logFile, date('[Y-m-d H:i:s] ') . "Ошибка: Неверный метод запроса\n", FILE_APPEND);
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
}

// Получение данных запроса
$player = isset($_POST['player']) ? trim($_POST['player']) : '';
$reason = isset($_POST['reason']) ? trim($_POST['reason']) : 'Разбан через админ-панель';

// Проверка обязательных полей
if (empty($player)) {
    file_put_contents($logFile, date('[Y-m-d H:i:s] ') . "Ошибка: Имя игрока не указано\n", FILE_APPEND);
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Player name is required']);
    exit;
}

try {
    // Настройки API Pterodactyl
    $pterodactyl_api_key = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV';
    $server_url = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command';

    // Формирование команды для разбана
    $command = "unban {$player} {$reason}";

    // Подготовка данных для запроса
    $data = json_encode(['command' => $command]);

    // Записываем информацию о запросе в лог
    file_put_contents(
        $logFile, 
        date('[Y-m-d H:i:s] ') . "Запрос к API Pterodactyl:\n" .
        "URL: $server_url\n" .
        "Команда: $command\n" .
        "Данные: $data\n",
        FILE_APPEND
    );

    // Инициализация cURL
    $ch = curl_init($server_url);

    // Настройка параметров cURL
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

    // Включаем подробное логирование
    curl_setopt($ch, CURLOPT_VERBOSE, true);
    $verbose = fopen('php://temp', 'w+');
    curl_setopt($ch, CURLOPT_STDERR, $verbose);

    // Выполнение запроса
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    $info = curl_getinfo($ch);

    // Более подробное логирование ответа и информации о запросе
    file_put_contents(
        $logFile, 
        date('[Y-m-d H:i:s] ') . "Детальная информация cURL:\n" .
        print_r($info, true) . "\n",
        FILE_APPEND
    );

    // Получение подробного лога
    rewind($verbose);
    $verbose_log = stream_get_contents($verbose);
    fclose($verbose);

    // Записываем результат запроса в лог
    file_put_contents(
        $logFile, 
        date('[Y-m-d H:i:s] ') . "Результат запроса:\n" .
        "HTTP код: $http_code\n" .
        "Ответ: " . ($response ?: 'Пустой ответ') . "\n" .
        ($error ? "Ошибка cURL: $error\n" : "") . 
        "Подробный лог cURL: $verbose_log\n",
        FILE_APPEND
    );

    // Закрытие cURL сессии
    curl_close($ch);

    // Проверка и обработка ответа
    if ($response === false) {
        throw new Exception('Failed to execute cURL request: ' . $error);
    }

    // Проверяем, пустой ли ответ (HTTP 204)
    if ($http_code === 204) {
        // HTTP 204 означает успешное выполнение без содержимого в ответе
        $response_data = ['success' => true];
        
        file_put_contents(
            $logFile, 
            date('[Y-m-d H:i:s] ') . "Получен HTTP 204 (No Content) - запрос успешно обработан\n",
            FILE_APPEND
        );
    } else {
        // Попытка декодировать JSON-ответ
        $response_data = json_decode($response, true);
        
        // Записываем декодированный ответ в лог
        file_put_contents(
            $logFile, 
            date('[Y-m-d H:i:s] ') . "Декодированный JSON ответ:\n" .
            print_r($response_data, true) . "\n",
            FILE_APPEND
        );

        // Проверка на ошибки декодирования JSON
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception('JSON decode error: ' . json_last_error_msg() . ' Response: ' . substr($response, 0, 1000));
        }
    }

    // Определяем результат операции
    if ($http_code >= 200 && $http_code < 300) {
        $result = [
            'status' => 'success',
            'message' => "Игрок $player успешно разбанен!",
            'details' => [
                'player' => $player,
                'reason' => $reason,
                'command' => $command,
                'http_code' => $http_code,
                'response' => $response_data
            ]
        ];
    } else {
        $result = [
            'status' => 'error',
            'message' => $error ? "Ошибка подключения: $error" : "Ошибка API: HTTP $http_code",
            'details' => [
                'player' => $player,
                'reason' => $reason,
                'command' => $command,
                'http_code' => $http_code,
                'error' => $error,
                'response' => $response_data
            ]
        ];
    }

} catch (Exception $e) {
    // Логирование исключения
    file_put_contents(
        $logFile, 
        date('[Y-m-d H:i:s] ') . "Исключение: " . $e->getMessage() . "\n" .
        "Трассировка стека: " . $e->getTraceAsString() . "\n",
        FILE_APPEND
    );

    // Возвращаем сообщение об ошибке клиенту
    $result = [
        'status' => 'error',
        'message' => 'Произошла ошибка при обработке запроса: ' . $e->getMessage(),
        'details' => [
            'player' => $player,
            'reason' => $reason,
            'error' => $e->getMessage()
        ]
    ];
}

// Записываем итоговый результат в лог
file_put_contents(
    $logFile, 
    date('[Y-m-d H:i:s] ') . "Отправляем ответ клиенту: " . json_encode($result) . "\n" .
    "===== ЗАВЕРШЕНИЕ СКРИПТА РАЗБАНА =====\n\n",
    FILE_APPEND
);

// Отправка ответа клиенту
header('Content-Type: application/json');
echo json_encode($result);
?>
