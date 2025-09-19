<?php
// Этот скрипт выполняет тестовый запрос к API Pterodactyl
header('Content-Type: text/plain');

echo "Тестовый запрос к API Pterodactyl\n\n";

// Настройки API
$api_key = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV';
$server_url = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command';
$test_player = 'TestPlayer';
$test_reason = 'Test unban';

// Формирование команды
$command = "unban {$test_player} {$test_reason}";
$data = json_encode(['command' => $command]);

echo "Отправка команды: $command\n";
echo "URL: $server_url\n";
echo "API Key: " . substr($api_key, 0, 10) . "...\n\n";

// Инициализация cURL
$ch = curl_init($server_url);

// Настройка параметров cURL
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Accept: Application/vnd.pterodactyl.v1+json',
    'Authorization: Bearer ' . $api_key
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 30);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

// Выполнение запроса
echo "Выполнение запроса...\n";
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
$info = curl_getinfo($ch);

echo "Ответ получен:\n";
echo "HTTP код: $http_code\n";
echo "Ошибка cURL: " . ($error ?: "Нет ошибок") . "\n\n";

echo "Детальная информация cURL:\n";
print_r($info);
echo "\n\n";

echo "Сырой ответ:\n";
echo $response;
echo "\n\n";

// Попытка декодировать JSON
$decoded = json_decode($response, true);
echo "Декодированный JSON:\n";
print_r($decoded);
echo "\n\n";

if (json_last_error() !== JSON_ERROR_NONE) {
    echo "Ошибка декодирования JSON: " . json_last_error_msg() . "\n";
}

curl_close($ch);
?>
