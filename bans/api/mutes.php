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
        'mutes' => [],
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
    $tableCheckResult = $conn->query("SHOW TABLES LIKE 'litebans_mutes'");
    if ($tableCheckResult->num_rows == 0) {
        // Таблица не существует
        echo json_encode([
            'mutes' => [],
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
    $sql = "SELECT m.id, m.uuid, m.reason, m.banned_by_name as muted_by_name, m.time, m.until, m.active, 
            m.removed_by_name, m.removed_by_reason, m.removed_by_date,
            (SELECT name FROM litebans_history WHERE uuid = m.uuid ORDER BY date DESC LIMIT 1) as player_name
            FROM litebans_mutes m
            WHERE 1=1";

    // Добавление условия поиска, если оно задано
    if (!empty($search)) {
        $search = $conn->real_escape_string($search);
        $sql .= " AND ((SELECT name FROM litebans_history WHERE uuid = m.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                OR m.banned_by_name LIKE '%$search%' OR m.reason LIKE '%$search%')";
    }

    // Добавление сортировки и ограничения для пагинации
    $sql .= " ORDER BY m.id DESC LIMIT $limit OFFSET $offset";

    // Выполнение запроса
    $result = $conn->query($sql);

    // Подготовка массива для результатов
    $mutes = [];

    // Обработка результатов
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            // Подготовка данных времени
            $time_value = 0;
            if (isset($row['time']) && is_numeric($row['time'])) {
                // Если таймстемп в миллисекундах (13+ знаков), конвертируем
                $time_value = strlen($row['time']) > 10 ? floor($row['time'] / 1000) : intval($row['time']);
            }
            
            // Подготовка данных даты окончания
            $until_value = 0;
            if (isset($row['until']) && is_numeric($row['until'])) {
                // Если таймстемп в миллисекундах (13+ знаков), конвертируем
                $until_value = strlen($row['until']) > 10 ? floor($row['until'] / 1000) : intval($row['until']);
            }
            
            // Проверяем наличие доказательств для мута
            $proofSql = "SELECT COUNT(*) as proof_count FROM litebans_mute_proof WHERE mute_id = {$row['id']}";
            $proofResult = $conn->query($proofSql);
            $hasProof = false;
            
            if ($proofResult) {
                $proofData = $proofResult->fetch_assoc();
                $hasProof = $proofData['proof_count'] > 0;
            }
            
            // Правильно определяем статус мута
            // Для MySQL значение bit(1) типа нужно преобразовывать в число
            $isActive = (int)$row['active'] === 1;
            
            // Формируем статус
            $status = $isActive ? 'Faol' : 'Tugagan';
            
            // ВАЖНО: Если мут все еще активен, очистим поля removed_by,
            // чтобы избежать путаницы в интерфейсе
            if ($isActive) {
                $row['removed_by_name'] = null;
                $row['removed_by_reason'] = null;
            } else {
                // Если мут неактивен, но поля removed_by пустые, значит срок истек автоматически
                if (empty($row['removed_by_name'])) {
                    $row['removed_by_name'] = 'System';
                    $row['removed_by_reason'] = 'Mute expired';
                }
            }
            
            // Поддерживаем и старый, и новый формат для обратной совместимости
            $mutes[] = [
                // Старый формат
                'id' => $row['id'],
                'player_name' => $row['player_name'] ?? 'Unknown Player',
                'uuid' => $row['uuid'],
                'reason' => $row['reason'],
                'muted_by_name' => $row['muted_by_name'] ?? 'Console',
                'time' => $time_value,
                'until' => $until_value,
                'active' => $isActive,
                
                // Новый формат
                'username' => $row['player_name'] ?? 'Unknown Player',
                'admin' => $row['muted_by_name'] ?? 'Console',
                'status' => $status,
                'type' => 'mute',
                'removed_by_name' => $row['removed_by_name'],
                'removed_by_reason' => $row['removed_by_reason'],
                'has_proof' => $hasProof,
                'date' => date('d.m.Y H:i', $time_value),
                'expires' => $until_value == 0 ? 'Doimiy' : date('d.m.Y H:i', $until_value)
            ];
        }
    }

    // Получение общего количества мутов для пагинации
    $countSql = "SELECT COUNT(*) as total FROM litebans_mutes";
    if (!empty($search)) {
        $countSql .= " WHERE ((SELECT name FROM litebans_history WHERE uuid = litebans_mutes.uuid ORDER BY date DESC LIMIT 1) LIKE '%$search%' 
                    OR banned_by_name LIKE '%$search%' OR reason LIKE '%$search%')";
    }
    $countResult = $conn->query($countSql);
    $totalMutes = $countResult ? $countResult->fetch_assoc()['total'] : 0;
    $totalPages = ceil($totalMutes / $limit);

    // Формирование и вывод JSON-ответа
    echo json_encode([
        'mutes' => $mutes,
        'pagination' => [
            'current_page' => $page,
            'total_pages' => $totalPages,
            'total_items' => $totalMutes,
            'limit' => $limit
        ]
    ]);

} catch (Exception $e) {
    // В случае любой ошибки возвращаем пустой массив
    echo json_encode([
        'mutes' => [],
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
