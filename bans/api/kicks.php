<?php
// Подключение к базе данных
require_once '../config/db.php';

// Установка заголовков для JSON
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');

// Получение параметров из запроса
$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 10;
$search = isset($_GET['search']) ? $_GET['search'] : '';

// Проверка соединения
if ($conn->connect_error) {
    echo json_encode([
        'kicks' => [],
        'pagination' => [
            'current_page' => $page,
            'total_pages' => 0,
            'total_items' => 0,
            'limit' => $limit
        ]
    ]);
    exit;
}

try {
    // Вычисление смещения для пагинации
    $offset = ($page - 1) * $limit;

    // Проверка существования таблицы
    $tableCheckResult = $conn->query("SHOW TABLES LIKE 'litebans_kicks'");
    if ($tableCheckResult->num_rows == 0) {
        // Таблица не существует
        echo json_encode([
            'kicks' => [],
            'pagination' => [
                'current_page' => $page,
                'total_pages' => 0,
                'total_items' => 0,
                'limit' => $limit
            ]
        ]);
        exit;
    }

    // Базовый SQL запрос
    $sql = "SELECT k.id, k.uuid, k.reason, k.banned_by_name as kicked_by_name, k.time, 
            (SELECT name FROM litebans_history WHERE uuid = k.uuid ORDER BY date DESC LIMIT 1) as player_name
            FROM litebans_kicks k
            WHERE 1=1";

    // Добавление условия поиска, если оно задано
    if (!empty($search)) {
        $search = $conn->real_escape_string($search);
        $sql .= " AND ((SELECT name FROM litebans_history WHERE uuid = k.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                OR k.banned_by_name LIKE '%$search%' OR k.reason LIKE '%$search%')";
    }

    // Добавление сортировки и ограничения для пагинации
    $sql .= " ORDER BY k.id DESC LIMIT $limit OFFSET $offset";

    // Выполнение запроса
    $result = $conn->query($sql);

    // Подготовка массива для результатов
    $kicks = [];

    // Обработка результатов
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            // Подготовка данных
            $time_value = 0;
            if (isset($row['time']) && is_numeric($row['time'])) {
                // Если таймстемп в миллисекундах (13+ знаков), конвертируем
                $time_value = strlen($row['time']) > 10 ? floor($row['time'] / 1000) : intval($row['time']);
            }
            
            // Добавляем данные
            $kicks[] = [
                'id' => $row['id'],
                'player_name' => $row['player_name'] ?? 'Unknown',
                'uuid' => $row['uuid'],
                'reason' => $row['reason'],
                'kicked_by_name' => $row['kicked_by_name'] ?? 'Console',
                'time' => $time_value,
                'until' => 0, // Для киков нет даты окончания
                'active' => false // Кики всегда неактивны
            ];
        }
    }

    // Получение общего количества киков для пагинации
    $countSql = "SELECT COUNT(*) as total FROM litebans_kicks";
    if (!empty($search)) {
        $countSql .= " WHERE ((SELECT name FROM litebans_history WHERE uuid = litebans_kicks.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                    OR banned_by_name LIKE '%$search%' OR reason LIKE '%$search%')";
    }
    $countResult = $conn->query($countSql);
    $totalKicks = $countResult ? $countResult->fetch_assoc()['total'] : 0;
    $totalPages = ceil($totalKicks / $limit);

    // Формирование и вывод JSON-ответа
    echo json_encode([
        'kicks' => $kicks,
        'pagination' => [
            'current_page' => $page,
            'total_pages' => $totalPages,
            'total_items' => $totalKicks,
            'limit' => $limit
        ]
    ]);

} catch (Exception $e) {
    // В случае любой ошибки возвращаем пустой массив
    echo json_encode([
        'kicks' => [],
        'pagination' => [
            'current_page' => $page,
            'total_pages' => 0,
            'total_items' => 0,
            'limit' => $limit
        ],
        'error' => $e->getMessage() // Для отладки
    ]);
}

// Закрытие соединения
$conn->close();
?>
