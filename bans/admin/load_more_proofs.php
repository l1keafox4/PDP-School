<?php
// Подключение к базе данных
include '../includes/db.php';

// Проверяем входные параметры
$section = isset($_GET['section']) ? $_GET['section'] : 'banlar';
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 20;
$limit = 20; // Количество записей для загрузки

// Отладочная информация
error_log("Load More Proofs request: section=$section, offset=$offset, limit=$limit");

// Проверка подключения
if ($conn->connect_error) {
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Connection failed: ' . $conn->connect_error]);
    exit();
}

// Установка заголовка ответа
header('Content-Type: application/json');

// Массив для результата
$result = [];

try {
    if ($section === 'mutelar') {
        // Получение пруфов для мутов
        $muteProofsQuery = "SELECT p.id, p.mute_id, p.proof_type, p.proof_url, UNIX_TIMESTAMP() as timestamp_now, m.banned_by_name, 
            (SELECT h.name FROM litebans_history h WHERE h.uuid = m.uuid ORDER BY h.date DESC LIMIT 1) AS player_name,
            m.reason
            FROM litebans_mute_proof p 
            JOIN litebans_mutes m ON p.mute_id = m.id
            ORDER BY p.id DESC LIMIT ?, ?";
            
        error_log("Executing mute proofs query with offset=$offset, limit=$limit");
        $stmt = $conn->prepare($muteProofsQuery);
        $stmt->bind_param("ii", $offset, $limit);
        $stmt->execute();
        $proofs = $stmt->get_result();
        error_log("Mute proofs query executed successfully");
        
        while ($proof = $proofs->fetch_assoc()) {
            $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['mute_id'] : $proof['player_name'];
            $reason = !empty($proof['reason']) ? htmlspecialchars($proof['reason']) : "Chat qoidalarini buzganlik uchun";
            
            // Удаляем префикс "Admin izoh:" из причины
            if (preg_match('/\[Admin izoh:(.*?)\]/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/Admin izoh:(.*?)$/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/\[Admin izoh:(.*?)$/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/\[(.*?)\]/', $reason, $matches)) {
                $reason = trim($matches[1]);
            }
            
            // Если причина пустая после обработки, используем значение по умолчанию
            if (empty(trim($reason))) {
                $reason = "Chat qoidalarini buzganlik uchun";
            }
            
            $result[] = [
                'id' => $proof['id'],
                'mute_id' => $proof['mute_id'],
                'proof_type' => $proof['proof_type'],
                'proof_url' => $proof['proof_url'],
                'player_name' => htmlspecialchars($player_name),
                'reason' => $reason,
                'timestamp' => date('Y-m-d H:i:s', $proof['timestamp_now'])
            ];
        }
    } else {
        // Получение пруфов для банов
        $banProofsQuery = "SELECT p.id, p.ban_id, p.proof_type, p.proof_url, UNIX_TIMESTAMP() as timestamp_now, b.banned_by_name, 
            (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name,
            b.reason
            FROM litebans_proof p 
            JOIN litebans_bans b ON p.ban_id = b.id
            ORDER BY p.id DESC LIMIT ?, ?";
            
        error_log("Executing ban proofs query with offset=$offset, limit=$limit");
        $stmt = $conn->prepare($banProofsQuery);
        $stmt->bind_param("ii", $offset, $limit);
        $stmt->execute();
        $proofs = $stmt->get_result();
        error_log("Ban proofs query executed successfully");
        
        while ($proof = $proofs->fetch_assoc()) {
            $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['ban_id'] : $proof['player_name'];
            $reason = !empty($proof['reason']) ? htmlspecialchars($proof['reason']) : "Qoidani buzganlik uchun";
            
            // Удаляем префикс "Admin izoh:" из причины
            if (preg_match('/\[Admin izoh:(.*?)\]/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/Admin izoh:(.*?)$/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/\[Admin izoh:(.*?)$/', $reason, $matches)) {
                $reason = trim($matches[1]);
            } elseif (preg_match('/\[(.*?)\]/', $reason, $matches)) {
                $reason = trim($matches[1]);
            }
            
            // Если причина пустая после обработки, используем значение по умолчанию
            if (empty(trim($reason))) {
                $reason = "Qoidani buzganlik uchun";
            }
            
            $result[] = [
                'id' => $proof['id'],
                'ban_id' => $proof['ban_id'],
                'proof_type' => $proof['proof_type'],
                'proof_url' => $proof['proof_url'],
                'player_name' => htmlspecialchars($player_name),
                'reason' => $reason,
                'timestamp' => date('Y-m-d H:i:s', $proof['timestamp_now'])
            ];
        }
    }
    
    error_log("Returning " . count($result) . " records");
    echo json_encode($result);
    
} catch (Exception $e) {
    error_log("Error in load_more_proofs.php: " . $e->getMessage());
    echo json_encode(['error' => 'Ошибка: ' . $e->getMessage()]);
}
?>
