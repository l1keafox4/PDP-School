<?php
// Подключение к базе данных
include '../includes/db.php';

// Выводим все данные для отладки
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Тестирование запроса для пагинации</h1>";

// Параметры запроса
$offset = 0;
$limit = 10;

echo "<p>Тестируем запрос с offset=$offset, limit=$limit</p>";

// Запрос для банов
$banProofsQuery = "SELECT p.id, p.ban_id, p.proof_type, p.proof_url, UNIX_TIMESTAMP() as timestamp_now, b.banned_by_name, 
    (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name,
    b.reason
    FROM litebans_proof p 
    JOIN litebans_bans b ON p.ban_id = b.id
    ORDER BY p.id DESC LIMIT ?, ?";

try {
    $stmt = $conn->prepare($banProofsQuery);
    $stmt->bind_param("ii", $offset, $limit);
    $stmt->execute();
    $proofs = $stmt->get_result();
    
    echo "<p>Запрос выполнен успешно. Получено записей: " . $proofs->num_rows . "</p>";
    
    echo "<h2>Результаты:</h2>";
    echo "<table border='1'>";
    echo "<tr><th>ID</th><th>Ban ID</th><th>Player</th><th>Reason</th></tr>";
    
    while ($proof = $proofs->fetch_assoc()) {
        $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['ban_id'] : $proof['player_name'];
        echo "<tr>";
        echo "<td>" . $proof['id'] . "</td>";
        echo "<td>" . $proof['ban_id'] . "</td>";
        echo "<td>" . htmlspecialchars($player_name) . "</td>";
        echo "<td>" . htmlspecialchars($proof['reason']) . "</td>";
        echo "</tr>";
    }
    
    echo "</table>";
    
} catch (Exception $e) {
    echo "<p style='color:red'>Ошибка: " . $e->getMessage() . "</p>";
}

// Теперь проверим запрос для смещения
$offset = 10;
echo "<h2>Тестируем запрос со смещением (offset=$offset)</h2>";

try {
    $stmt = $conn->prepare($banProofsQuery);
    $stmt->bind_param("ii", $offset, $limit);
    $stmt->execute();
    $proofs = $stmt->get_result();
    
    echo "<p>Запрос выполнен успешно. Получено записей: " . $proofs->num_rows . "</p>";
    
    echo "<h2>Результаты:</h2>";
    echo "<table border='1'>";
    echo "<tr><th>ID</th><th>Ban ID</th><th>Player</th><th>Reason</th></tr>";
    
    while ($proof = $proofs->fetch_assoc()) {
        $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['ban_id'] : $proof['player_name'];
        echo "<tr>";
        echo "<td>" . $proof['id'] . "</td>";
        echo "<td>" . $proof['ban_id'] . "</td>";
        echo "<td>" . htmlspecialchars($player_name) . "</td>";
        echo "<td>" . htmlspecialchars($proof['reason']) . "</td>";
        echo "</tr>";
    }
    
    echo "</table>";
    
} catch (Exception $e) {
    echo "<p style='color:red'>Ошибка: " . $e->getMessage() . "</p>";
}
?>
