<?php
// Усиленные заголовки для полного предотвращения кэширования
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header("Expires: 0");
header('Content-Type: application/json; charset=utf-8');

// Дополнительные заголовки для клиентских кэшей
header('Cache-Control: private, no-store, max-age=0, no-cache, must-revalidate, post-check=0, pre-check=0');
header('Expires: Sat, 26 Jul 1997 05:00:00 GMT');
header('Pragma: no-cache');

// Подключение к базе данных
require_once '../config/db.php';

// Установка заголовков для JSON
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

// Получение параметров из запроса
$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 10;
$search = isset($_GET['search']) ? $_GET['search'] : '';

// Вычисление смещения для пагинации
$offset = ($page - 1) * $limit;

// Базовый SQL запрос - добавляем сортировку по ID для гарантии последних банов
$sql = "SELECT b.id, b.uuid, b.reason, b.banned_by_name, b.time, b.until, b.active, 
        b.removed_by_name, b.removed_by_reason, b.removed_by_date,
        (SELECT name FROM litebans_history WHERE uuid = b.uuid ORDER BY date DESC LIMIT 1) as player_name
        FROM litebans_bans b
        WHERE 1=1";

// Добавление условия поиска, если оно задано
if (!empty($search)) {
    $search = $conn->real_escape_string($search);
    $sql .= " AND ((SELECT name FROM litebans_history WHERE uuid = b.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
              OR b.banned_by_name LIKE '%$search%' OR b.reason LIKE '%$search%')";
}

// Добавление сортировки и ограничения для пагинации
// Используем сортировку по ID (первичный ключ) для гарантии правильного порядка
$sql .= " ORDER BY b.id DESC LIMIT $limit OFFSET $offset";

// Выполнение запроса
$result = $conn->query($sql);

// Проверка наличия ошибок
if (!$result) {
    echo json_encode(['error' => 'Ошибка запроса: ' . $conn->error]);
    exit;
}

// Подготовка массива для результатов
$bans = [];

// Обработка результатов
while ($row = $result->fetch_assoc()) {
    // Проверяем наличие доказательств для бана
    $proofSql = "SELECT COUNT(*) as proof_count FROM litebans_proof WHERE ban_id = {$row['id']}";
    $proofResult = $conn->query($proofSql);
    $hasProof = false;
    
    if ($proofResult) {
        $proofData = $proofResult->fetch_assoc();
        $hasProof = $proofData['proof_count'] > 0;
    }
    
    // Правильно определяем статус бана
    // Для MySQL значение bit(1) типа нужно преобразовывать в число
    $isActive = (int)$row['active'] === 1;
    
    // Формируем статус
    $status = $isActive ? 'Faol' : 'Tugagan';
    
    // ВАЖНО: Если бан все еще активен, очистим поля removed_by,
    // чтобы избежать путаницы в интерфейсе
    if ($isActive) {
        $row['removed_by_name'] = null;
        $row['removed_by_reason'] = null;
    } else {
        // Если бан неактивен, но поля removed_by пустые, значит срок истек автоматически
        if (empty($row['removed_by_name'])) {
            $row['removed_by_name'] = 'System';
            $row['removed_by_reason'] = 'Ban expired';
        }
    }
    
    // Поддерживаем и старый, и новый формат для обратной совместимости
    $bans[] = [
        // Старый формат
        'id' => $row['id'],
        'player_name' => $row['player_name'] ?? 'Unknown Player',
        'uuid' => $row['uuid'],
        'reason' => $row['reason'],
        'banned_by_name' => $row['banned_by_name'],
        'time' => $row['time'],
        'until' => $row['until'],
        'active' => $isActive,
        
        // Новый формат
        'username' => $row['player_name'] ?? 'Unknown Player',
        'admin' => $row['banned_by_name'],
        'status' => $status,
        'type' => 'ban',
        'removed_by_name' => $row['removed_by_name'],
        'removed_by_reason' => $row['removed_by_reason'],
        'has_proof' => $hasProof,
        'date' => date('d.m.Y H:i', is_numeric($row['time']) ? (strlen($row['time']) > 10 ? floor($row['time'] / 1000) : $row['time']) : time()),
        'expires' => $row['until'] == 0 ? 'Doimiy' : date('d.m.Y H:i', strlen($row['until']) > 10 ? floor($row['until'] / 1000) : $row['until'])
    ];
}

// Получение общего количества банов для пагинации
$countSql = "SELECT COUNT(*) as total FROM litebans_bans";
if (!empty($search)) {
    $countSql .= " WHERE ((SELECT name FROM litebans_history WHERE uuid = litebans_bans.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                  OR banned_by_name LIKE '%$search%' OR reason LIKE '%$search%')";
}
$countResult = $conn->query($countSql);
$totalBans = $countResult->fetch_assoc()['total'];
$totalPages = ceil($totalBans / $limit);

// Формирование и вывод JSON-ответа
echo json_encode([
    'bans' => $bans,
    'pagination' => [
        'current_page' => $page,
        'total_pages' => $totalPages,
        'total_items' => $totalBans,
        'limit' => $limit
    ]
]);

// Закрытие соединения
$conn->close();
?>
