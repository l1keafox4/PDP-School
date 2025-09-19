<?php
// Подключение к базе данных
require_once '../config/db.php';

// Установка заголовков для JSON
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

// Получение параметров из запроса
$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 10;
$search = isset($_GET['search']) ? $_GET['search'] : '';

// Вычисление смещения для пагинации
$offset = ($page - 1) * $limit;

// Базовый SQL запрос
$sql = "SELECT w.id, w.uuid, w.reason, w.banned_by_name, w.time, w.until, w.active, 
        (SELECT name FROM litebans_history WHERE uuid = w.uuid ORDER BY date DESC LIMIT 1) as player_name
        FROM litebans_warnings w
        WHERE 1=1";

// Добавление условия поиска, если оно задано
if (!empty($search)) {
    $search = $conn->real_escape_string($search);
    $sql .= " AND ((SELECT name FROM litebans_history WHERE uuid = w.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
              OR w.banned_by_name LIKE '%$search%' OR w.reason LIKE '%$search%')";
}

// Добавление сортировки и ограничения для пагинации
$sql .= " ORDER BY w.time DESC LIMIT $limit OFFSET $offset";

// Выполнение запроса
$result = $conn->query($sql);

// Проверка наличия ошибок
if (!$result) {
    echo json_encode(['error' => 'Ошибка запроса: ' . $conn->error]);
    exit;
}

// Подготовка массива для результатов
$warnings = [];

// Обработка результатов
while ($row = $result->fetch_assoc()) {
    // Преобразование временных меток Unix в читаемый формат
    $timeCreated = date('d/m/Y, h:i A', $row['time'] / 1000);
    
    // Определение времени окончания предупреждения
    if ($row['until'] == 0) {
        $timeUntil = 'Навсегда';
    } else {
        $timeUntil = date('d/m/Y, h:i A', $row['until'] / 1000);
    }
    
    // Определение статуса предупреждения
    $status = $row['active'] ? 'Faol' : 'Tugagan';
    $statusClass = $row['active'] ? 'orange' : 'gray';
    
    // Добавление данных в массив
    $warnings[] = [
        'id' => $row['id'],
        'player_name' => $row['player_name'] ?? 'Unknown',
        'uuid' => $row['uuid'],
        'reason' => $row['reason'],
        'admin' => $row['banned_by_name'],
        'time_created' => $timeCreated,
        'time_until' => $timeUntil,
        'status' => $status,
        'status_class' => $statusClass
    ];
}

// Получение общего количества предупреждений для пагинации
$countSql = "SELECT COUNT(*) as total FROM litebans_warnings";
if (!empty($search)) {
    $countSql .= " WHERE ((SELECT name FROM litebans_history WHERE uuid = litebans_warnings.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                  OR banned_by_name LIKE '%$search%' OR reason LIKE '%$search%')";
}
$countResult = $conn->query($countSql);
$totalWarnings = $countResult->fetch_assoc()['total'];
$totalPages = ceil($totalWarnings / $limit);

// Формирование и вывод JSON-ответа
echo json_encode([
    'warnings' => $warnings,
    'pagination' => [
        'current_page' => $page,
        'total_pages' => $totalPages,
        'total_items' => $totalWarnings,
        'limit' => $limit
    ]
]);

// Закрытие соединения
$conn->close();
?>
