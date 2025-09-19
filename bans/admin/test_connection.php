<?php
// Скрипт для тестирования соединения с плагином Minecraft
header('Content-Type: text/html; charset=utf-8');

echo "<h1>Тест соединения с плагином UnbanPlugin</h1>";

// Параметры соединения
$serverHost = "37.27.96.155";
$serverPort = 4545;

// Тестовые данные
$testData = [
    'player' => 'TestPlayer',
    'reason' => 'Connection test',
    'admin'  => 'TestAdminPanel'
];

echo "<h2>Тест 1: базовая проверка доступности порта</h2>";
$socket = @fsockopen($serverHost, $serverPort, $errno, $errstr, 5);
if (!$socket) {
    echo "<p style='color:red'>Ошибка соединения: $errstr ($errno)</p>";
} else {
    echo "<p style='color:green'>Успешное соединение с $serverHost:$serverPort</p>";
    fclose($socket);
}

echo "<h2>Тест 2: отправка HTTP запроса через socket</h2>";
$socket = @fsockopen($serverHost, $serverPort, $errno, $errstr, 5);
if (!$socket) {
    echo "<p style='color:red'>Ошибка соединения: $errstr ($errno)</p>";
} else {
    $data = json_encode($testData);
    
    $request = "POST / HTTP/1.1\r\n";
    $request .= "Host: $serverHost:$serverPort\r\n";
    $request .= "Content-Type: application/json\r\n";
    $request .= "Content-Length: " . strlen($data) . "\r\n";
    $request .= "Connection: Close\r\n\r\n";
    $request .= $data;
    
    echo "<p>Отправка запроса:</p>";
    echo "<pre>" . htmlspecialchars($request) . "</pre>";
    
    fwrite($socket, $request);
    
    $response = '';
    while (!feof($socket)) {
        $response .= fgets($socket, 128);
    }
    fclose($socket);
    
    echo "<p>Получен ответ:</p>";
    echo "<pre>" . htmlspecialchars($response) . "</pre>";
}

echo "<h2>Тест 3: отправка через cURL</h2>";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://$serverHost:$serverPort/");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($testData));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_VERBOSE, true);

$verbose = fopen('php://temp', 'w+');
curl_setopt($ch, CURLOPT_STDERR, $verbose);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);

rewind($verbose);
$verboseLog = stream_get_contents($verbose);
fclose($verbose);

echo "<p>Код ответа: $httpCode</p>";
if ($error) {
    echo "<p style='color:red'>Ошибка cURL: $error</p>";
} else {
    echo "<p style='color:green'>cURL запрос выполнен успешно</p>";
}

echo "<p>Подробный лог cURL:</p>";
echo "<pre>" . htmlspecialchars($verboseLog) . "</pre>";

echo "<p>Ответ:</p>";
echo "<pre>" . htmlspecialchars($response) . "</pre>";

curl_close($ch);

echo "<h2>Тест 4: Проверка файервола</h2>";
// Проверка наличия iptables
$iptablesExists = shell_exec('which iptables');
if ($iptablesExists) {
    echo "<p>iptables найден в системе</p>";
    
    // Проверка правил для порта 4545
    $iptablesRules = shell_exec('iptables -L -n | grep 4545');
    echo "<p>Правила iptables для порта 4545:</p>";
    echo "<pre>" . ($iptablesRules ?: "Правила не найдены") . "</pre>";
} else {
    echo "<p>iptables не найден в системе</p>";
}

// Проверка открытых портов
$netstatOutput = shell_exec('netstat -tulpn | grep 4545');
echo "<p>Открытые порты 4545:</p>";
echo "<pre>" . ($netstatOutput ?: "Порт не найден в списке прослушиваемых") . "</pre>";

echo "<h2>Рекомендации</h2>";
echo "<ul>";
echo "<li>Проверьте настройки плагина в config.yml (правильный ли порт указан)</li>";
echo "<li>Проверьте, что плагин успешно запустился и слушает порт 4545</li>";
echo "<li>Убедитесь, что брандмауэр сервера разрешает соединения на порт 4545</li>";
echo "<li>Проверьте логи сервера Minecraft на наличие ошибок</li>";
echo "</ul>";

echo "<p><a href='javascript:void(0)' onclick='window.location.reload()'>Повторить тесты</a></p>";
?>
