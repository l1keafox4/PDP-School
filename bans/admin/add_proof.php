<?php
include 'auth.php';
include 'db_config.php';

// Проверка, авторизован ли пользователь
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}

// Сообщения
$message = '';
$success = '';
$error = '';

// Обработка отправки формы
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['add_proof'])) {
    $ban_id = $_POST['ban_id'] ?? '';
    $proof_link = $_POST['proof_link'] ?? '';
    
    // Проверка данных
    if (empty($ban_id) || empty($proof_link)) {
        $error = 'Заполните все поля';
    } else {
        // Получаем информацию о бане
        $check_ban = $conn->prepare("SELECT id, uuid, time FROM litebans_bans WHERE id = ? AND active = 1");
        $check_ban->bind_param("i", $ban_id);
        $check_ban->execute();
        $result = $check_ban->get_result();
        
        if ($result->num_rows === 0) {
            $error = "Бан с ID $ban_id не найден или не активен";
        } else {
            // Проверяем, не добавлен ли уже пруф для этого бана
            $check_proof = $conn->prepare("SELECT id FROM litebans_ban_proofs WHERE ban_id = ?");
            $check_proof->bind_param("i", $ban_id);
            $check_proof->execute();
            $proof_result = $check_proof->get_result();
            
            if ($proof_result->num_rows > 0) {
                $error = "Пруф для этого бана уже добавлен";
            } else {
                try {
                    // Создаем таблицу для пруфов, если её нет
                    $conn->query("
                        CREATE TABLE IF NOT EXISTS litebans_ban_proofs (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            ban_id INT NOT NULL,
                            admin_name VARCHAR(255) NOT NULL,
                            proof_link TEXT NOT NULL,
                            time BIGINT NOT NULL,
                            UNIQUE KEY (ban_id)
                        )
                    ");
                    
                    // Добавляем пруф
                    $insert = $conn->prepare("INSERT INTO litebans_ban_proofs (ban_id, admin_name, proof_link, time) VALUES (?, ?, ?, ?)");
                    $admin_name = $_SESSION['username'];
                    $current_time = time() * 1000; // в миллисекундах как в LiteBans
                    $insert->bind_param("issi", $ban_id, $admin_name, $proof_link, $current_time);
                    
                    if ($insert->execute()) {
                        // Получаем информацию об игроке
                        $player_query = $conn->prepare("
                            SELECT h.name AS player_name
                            FROM litebans_bans b
                            LEFT JOIN litebans_history h ON b.uuid = h.uuid
                            WHERE b.id = ?
                        ");
                        $player_query->bind_param("i", $ban_id);
                        $player_query->execute();
                        $player_result = $player_query->get_result();
                        $player_info = $player_result->fetch_assoc();
                        $player_name = $player_info['player_name'] ?: "Игрок с ID $ban_id";
                        
                        // Логируем добавление пруфа
                        $log_file = __DIR__ . '/../PLUGIN_DEVELOPING/ban_activity.log';
                        $timestamp = date('[Y-m-d H:i:s]');
                        $log_message = "Пруф опубликован для игрока $player_name от админа $admin_name";
                        file_put_contents($log_file, "$timestamp $log_message\n", FILE_APPEND);
                        
                        $success = "Пруф успешно добавлен для бана с ID $ban_id";
                    } else {
                        $error = "Ошибка при добавлении пруфа: " . $insert->error;
                    }
                } catch (Exception $e) {
                    $error = "Ошибка: " . $e->getMessage();
                }
            }
        }
    }
}

// Получаем список последних активных банов без пруфов
$bans_query = "
    SELECT b.id, b.uuid, h.name AS player_name, b.banned_by_name, b.reason, b.time
    FROM litebans_bans b
    LEFT JOIN litebans_history h ON b.uuid = h.uuid
    LEFT JOIN (
        SELECT DISTINCT ban_id FROM litebans_ban_proofs
    ) p ON b.id = p.ban_id
    WHERE 
        b.active = 1
        AND p.ban_id IS NULL
    ORDER BY b.time DESC
    LIMIT 50
";

$bans_result = $conn->query($bans_query);
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Добавление пруфов - LiteBans Админ панель</title>
    <link rel="stylesheet" href="modern.css">
    <style>
        .container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 5px;
        }
        
        .bans-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .bans-table th, .bans-table td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        
        .bans-table th {
            background-color: #f5f5f5;
        }
        
        .bans-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .bans-table tr:hover {
            background-color: #f1f1f1;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .form-group input[type="text"],
        .form-group input[type="url"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .button-group {
            margin-top: 15px;
        }
        
        .button {
            padding: 8px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .button:hover {
            background-color: #0069d9;
        }
        
        .message {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        .success-message {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .deadline-passed {
            color: #dc3545;
            font-weight: bold;
        }
        
        .deadline-warning {
            color: #ffc107;
            font-weight: bold;
        }
        
        .deadline-ok {
            color: #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Добавление пруфов к банам</h1>
        
        <a href="index.php" class="button" style="margin-bottom: 20px; display: inline-block;">Вернуться в панель управления</a>
        
        <?php if (!empty($error)): ?>
            <div class="message error-message"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <?php if (!empty($success)): ?>
            <div class="message success-message"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <div class="form-container">
            <h2>Добавить пруф</h2>
            <form method="post" action="">
                <div class="form-group">
                    <label for="ban_id">ID бана:</label>
                    <input type="text" id="ban_id" name="ban_id" required>
                </div>
                
                <div class="form-group">
                    <label for="proof_link">Ссылка на пруф:</label>
                    <input type="url" id="proof_link" name="proof_link" required>
                </div>
                
                <div class="button-group">
                    <button type="submit" name="add_proof" class="button">Добавить пруф</button>
                </div>
            </form>
        </div>
        
        <h2>Последние баны без пруфов</h2>
        <?php if ($bans_result && $bans_result->num_rows > 0): ?>
            <table class="bans-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Игрок</th>
                        <th>Администратор</th>
                        <th>Причина</th>
                        <th>Время бана</th>
                        <th>Срок для пруфа</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($ban = $bans_result->fetch_assoc()): 
                        $ban_time = intval($ban['time'] / 1000);
                        $deadline_time = $ban_time + (2 * 60 * 60);
                        $current_time = time();
                        $time_left = $deadline_time - $current_time;
                        
                        // Определяем класс для срока
                        if ($time_left < 0) {
                            $deadline_class = 'deadline-passed';
                            $deadline_text = 'Просрочено!';
                        } elseif ($time_left < 30 * 60) { // менее 30 минут
                            $deadline_class = 'deadline-warning';
                            $deadline_text = 'Скоро истечет';
                        } else {
                            $deadline_class = 'deadline-ok';
                            $deadline_text = 'В пределах нормы';
                        }
                    ?>
                    <tr>
                        <td><?php echo $ban['id']; ?></td>
                        <td><?php echo htmlspecialchars($ban['player_name'] ?: 'Неизвестно'); ?></td>
                        <td><?php echo htmlspecialchars($ban['banned_by_name'] ?: 'Неизвестно'); ?></td>
                        <td><?php echo htmlspecialchars($ban['reason'] ?: 'Не указана'); ?></td>
                        <td><?php echo date('Y-m-d H:i:s', $ban_time); ?></td>
                        <td class="<?php echo $deadline_class; ?>">
                            <?php echo date('Y-m-d H:i:s', $deadline_time); ?>
                            <br>
                            <small><?php echo $deadline_text; ?></small>
                        </td>
                        <td>
                            <button class="button" onclick="fillForm(<?php echo $ban['id']; ?>)">Добавить пруф</button>
                        </td>
                    </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p>Нет активных банов без пруфов</p>
        <?php endif; ?>
    </div>
    
    <script>
        function fillForm(banId) {
            document.getElementById('ban_id').value = banId;
            document.getElementById('proof_link').focus();
            window.scrollTo(0, 0);
        }
    </script>
</body>
</html>
