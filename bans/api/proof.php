<?php
// Подключение к базе данных
$config_path = dirname(__FILE__) . '/../config/db.php';

// Проверка существования файла конфигурации
if (file_exists($config_path)) {
    require_once $config_path;
} else {
    // Если файл конфигурации не найден, используем прямое подключение
    $host = "65.109.116.247:3306";
    $username = "litebans";
    $password = "limon1232";
    $database = "litebans";
    
    // Создание соединения
    $conn = new mysqli($host, $username, $password, $database);
    
    // Проверка соединения
    if ($conn->connect_error) {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Ошибка подключения к базе данных: ' . $conn->connect_error]);
        exit;
    }
    
    // Установка кодировки
    $conn->set_charset("utf8mb4");
}

// Установка заголовков для JSON
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

// Получение параметров из запроса
$type = isset($_GET['type']) ? $_GET['type'] : '';
$id = isset($_GET['id']) ? intval($_GET['id']) : 0;
$player = isset($_GET['player']) ? $_GET['player'] : '';

// Проверка наличия необходимых параметров
if ((empty($type) || $id <= 0) && empty($player)) {
    echo json_encode(['error' => 'Необходимо указать тип (ban или mute) и ID, или имя игрока']);
    exit;
}

// Выбор таблицы в зависимости от типа
$table = '';
if ($type === 'ban') {
    $table = 'litebans_proof';
    $idField = 'ban_id';
} elseif ($type === 'mute') {
    $table = 'litebans_mute_proof';
    $idField = 'mute_id';
} else {
    echo json_encode(['error' => 'Неверный тип. Допустимые значения: ban, mute']);
    exit;
}

// SQL запрос для получения доказательств
$sql = "";
$playerInfo = null;

if (!empty($player)) {
    // Если указано имя игрока, ищем все доказательства для данного игрока
    // Сначала получаем ID наказаний этого игрока
    $playerTable = $type === 'ban' ? 'litebans_bans' : 'litebans_mutes';
    
    // Ищем наказания по имени или UUID
    $playerName = $conn->real_escape_string($player);
    $playerSql = "SELECT id, uuid, reason, banned_by_name FROM {$playerTable} 
                 WHERE (uuid LIKE '%{$playerName}%' OR reason LIKE '%{$playerName}%') 
                 AND active = b'1' 
                 ORDER BY time DESC";
    
    $playerResult = $conn->query($playerSql);
    
    if ($playerResult && $playerResult->num_rows > 0) {
        $ids = [];
        $playerInfo = $playerResult->fetch_assoc(); // Сохраняем информацию о первом найденном наказании
        $playerResult->data_seek(0); // Возвращаемся к началу результатов
        
        while ($row = $playerResult->fetch_assoc()) {
            $ids[] = $row['id'];
        }
        
        if (!empty($ids)) {
            $idsStr = implode(",", $ids);
            $sql = "SELECT p.id, p.{$idField}, p.proof_url, p.proof_type, p.created_at, p.admin_feedback, 
                    p.player_name, p.admin_name, p.reason,
                    b.uuid as player_uuid, b.reason as punishment_reason, b.banned_by_name as admin_name
                    FROM {$table} p
                    JOIN {$playerTable} b ON p.{$idField} = b.id
                    WHERE p.{$idField} IN ({$idsStr})
                    ORDER BY p.created_at DESC";
        }
    }
    
    // Если не нашли никаких ID, используем пустой запрос
    if (empty($sql)) {
        $sql = "SELECT id, {$idField}, proof_url, proof_type, created_at, admin_feedback 
               FROM {$table} 
               LIMIT 0";
    }
} else {
    // Обновленный запрос включая новые поля
    $sql = "SELECT id, {$idField}, proof_url, proof_type, created_at, admin_feedback, 
           player_name, admin_name, reason
           FROM {$table} 
           WHERE {$idField} = {$id}
           ORDER BY created_at DESC";
}

// Выполнение запроса
$result = $conn->query($sql);

// Проверка существования таблицы
$tableExists = $conn->query("SHOW TABLES LIKE '{$table}'")->num_rows > 0;
if (!$tableExists) {
    // Таблица не существует, создаем её
    $createTableSql = "";
    
    if ($table === 'litebans_proof') {
        $createTableSql = "CREATE TABLE IF NOT EXISTS litebans_proof (
            id INT(11) NOT NULL AUTO_INCREMENT,
            ban_id BIGINT(20) UNSIGNED NOT NULL,
            proof_url VARCHAR(2048) NOT NULL,
            proof_type VARCHAR(50) NOT NULL,
            admin_feedback TEXT NULL,
            player_name VARCHAR(255) DEFAULT NULL,
            admin_name VARCHAR(255) DEFAULT NULL,
            reason TEXT DEFAULT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY ban_id (ban_id)
        )";
    } else if ($table === 'litebans_mute_proof') {
        $createTableSql = "CREATE TABLE IF NOT EXISTS litebans_mute_proof (
            id INT(11) NOT NULL AUTO_INCREMENT,
            mute_id BIGINT(20) UNSIGNED NOT NULL,
            proof_url VARCHAR(2048) NOT NULL,
            proof_type VARCHAR(50) NOT NULL,
            admin_feedback TEXT NULL,
            player_name VARCHAR(255) DEFAULT NULL,
            admin_name VARCHAR(255) DEFAULT NULL,
            reason TEXT DEFAULT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY mute_id (mute_id)
        )";
    }
    
    if (!empty($createTableSql)) {
        $conn->query($createTableSql);
    }
}

// Проверка наличия ошибок
if (!$result) {
    echo json_encode([
        'error' => 'Ошибка запроса: ' . $conn->error,
        'debug' => [
            'query' => $sql,
            'table_exists' => $tableExists,
            'id_field' => $idField,
            'type' => $type,
            'id' => $id
        ]
    ]);
    exit;
}

// Подготовка массива для результатов
$proofs = [];

// Обработка результатов
while ($row = $result->fetch_assoc()) {
    // Добавляем дополнительные поля для совместимости с интерфейсом, только если они отсутствуют
    // Устанавливаем резервные значения только если поля пустые
    if (empty($row['player_uuid'])) {
        $row['player_uuid'] = 'player-' . $id;
    }
    
    // Используем реальные значения из таблицы litebans_proof
    if (empty($row['player_name'])) {
        $row['player_name'] = 'Неизвестный игрок';
    }
    
    if (empty($row['punishment_reason']) && empty($row['reason'])) {
        $row['punishment_reason'] = 'Подозрение в использовании читов';
    }
    
    if (empty($row['admin_name'])) {
        $row['admin_name'] = 'Console';
    }
    
    $proofs[] = $row;
}

// Формирование и вывод JSON-ответа
echo json_encode([
    'proofs' => $proofs,
    'count' => count($proofs),
    'player_info' => $playerInfo,
    'debug' => [
        'query' => $sql,
        'table' => $table,
        'id_field' => $idField,
        'type' => $type,
        'id' => $id,
        'player' => $player,
        'timestamp' => date('Y-m-d H:i:s')
    ]
]);

// Закрытие соединения
$conn->close();
?>
