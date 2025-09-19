<?php
include 'auth.php';
include 'db_config.php';

$player_name = isset($_GET['player']) ? $_GET['player'] : 'lido_unban_pliz';

// Запрос к базе данных для получения информации о бане
$query = $conn->prepare("
    SELECT b.id, b.uuid, b.banned_by_uuid, b.banned_by_name, b.reason, b.time, h.name as player_name
    FROM litebans_bans b
    LEFT JOIN litebans_history h ON b.uuid = h.uuid
    WHERE h.name = ? OR b.uuid = ?
    ORDER BY b.time DESC
    LIMIT 1
");

$query->bind_param("ss", $player_name, $player_name);
$query->execute();
$result = $query->get_result();

echo "<h1>Информация о бане игрока: $player_name</h1>";

if ($result->num_rows > 0) {
    $ban = $result->fetch_assoc();
    
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>ID бана</th><td>" . $ban['id'] . "</td></tr>";
    echo "<tr><th>UUID игрока</th><td>" . $ban['uuid'] . "</td></tr>";
    echo "<tr><th>Имя игрока</th><td>" . $ban['player_name'] . "</td></tr>";
    echo "<tr><th>Забанен админом (UUID)</th><td>" . $ban['banned_by_uuid'] . "</td></tr>";
    echo "<tr><th>Забанен админом (имя)</th><td>" . ($ban['banned_by_name'] ?: "Не указано") . "</td></tr>";
    echo "<tr><th>Причина</th><td>" . $ban['reason'] . "</td></tr>";
    
    // Форматируем время бана
    $ban_time = intval($ban['time'] / 1000);
    $formatted_time = date('Y-m-d H:i:s', $ban_time);
    echo "<tr><th>Время бана</th><td>" . $formatted_time . "</td></tr>";
    
    echo "</table>";
} else {
    echo "<p>Информация о бане игрока $player_name не найдена.</p>";
}
?>
