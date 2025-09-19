<?php
// Устанавливаем заголовки для вывода текста
header('Content-Type: text/plain');

echo "Начало выполнения тестового скрипта\n";

// Настройки API
$api_key = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV';
$url = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command';
$player = 'Unban_1'; // Тестовый игрок для разбана
$reason = 'Тест разбана';

echo "Отправка запроса к API: $url\n";
echo "Игрок: $player, Причина: $reason\n";

// Формируем команду
$command = "unban {$player} {$reason}";
$data = json_encode(['command' => $command]);

echo "Команда: $command\n";
echo "JSON данные: $data\n";

// Инициализируем cURL
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Accept: Application/vnd.pterodactyl.v1+json',
    'Authorization: Bearer ' . $api_key,
    'Content-Length: ' . strlen($data)
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

// Включаем подробное логирование
curl_setopt($ch, CURLOPT_VERBOSE, true);
$verbose = fopen('php://temp', 'w+');
curl_setopt($ch, CURLOPT_STDERR, $verbose);

echo "Отправка запроса...\n";

// Выполняем запрос
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);

// Получаем подробный лог
rewind($verbose);
$verbose_log = stream_get_contents($verbose);
fclose($verbose);

echo "HTTP код: $http_code\n";
echo "Ответ: " . ($response ?: 'Нет ответа') . "\n";

if ($error) {
    echo "Ошибка cURL: $error\n";
}

echo "Подробный лог cURL:\n$verbose_log\n";

curl_close($ch);

echo "Завершение тестового скрипта\n";
?>
