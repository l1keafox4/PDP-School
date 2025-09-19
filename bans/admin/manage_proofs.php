<?php
include 'auth.php';
include 'db_config.php';

// Сообщения
$success = '';
$error = '';

// Обработка удаления пруфа
if (isset($_GET['action']) && $_GET['action'] === 'delete' && isset($_GET['type']) && isset($_GET['id'])) {
    $type = $_GET['type'];
    $id = (int)$_GET['id'];
    
    if ($type === 'ban') {
        // Получаем информацию о пруфе перед удалением для проверки файла
        $proof = $conn->query("SELECT proof_url FROM litebans_proof WHERE id = $id")->fetch_assoc();
        
        if ($proof) {
            // Удаляем запись из базы данных
            if ($conn->query("DELETE FROM litebans_proof WHERE id = $id")) {
                $success = 'Пруф успешно удален';
                
                // Если это локальный файл, удаляем его
                $proof_url = $proof['proof_url'];
                if (strpos($proof_url, 'uploads/proofs/') === 0) {
                    $file_path = '../' . $proof_url;
                    if (file_exists($file_path)) {
                        unlink($file_path);
                    }
                }
            } else {
                $error = 'Ошибка при удалении пруфа';
            }
        } else {
            $error = 'Пруф не найден';
        }
    } elseif ($type === 'mute') {
        // Получаем информацию о пруфе перед удалением для проверки файла
        $proof = $conn->query("SELECT proof_url FROM litebans_mute_proof WHERE id = $id")->fetch_assoc();
        
        if ($proof) {
            // Удаляем запись из базы данных
            if ($conn->query("DELETE FROM litebans_mute_proof WHERE id = $id")) {
                $success = 'Пруф успешно удален';
                
                // Если это локальный файл, удаляем его
                $proof_url = $proof['proof_url'];
                if (strpos($proof_url, 'uploads/proofs/') === 0) {
                    $file_path = '../' . $proof_url;
                    if (file_exists($file_path)) {
                        unlink($file_path);
                    }
                }
            } else {
                $error = 'Ошибка при удалении пруфа';
            }
        } else {
            $error = 'Пруф не найден';
        }
    } else {
        $error = 'Неверный тип пруфа';
    }
}

// Пагинация
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$items_per_page = 10;
$offset = ($page - 1) * $items_per_page;

// Фильтрация
$filter_type = isset($_GET['filter_type']) ? $_GET['filter_type'] : 'all';
$filter_proof_type = isset($_GET['filter_proof_type']) ? $_GET['filter_proof_type'] : 'all';

// Подготовка запроса
$ban_query = "SELECT p.id, p.ban_id, p.proof_url, p.proof_type, p.uploaded_at, b.uuid, b.reason 
              FROM litebans_proof p 
              LEFT JOIN litebans_bans b ON p.ban_id = b.id";
$mute_query = "SELECT p.id, p.mute_id, p.proof_url, p.proof_type, p.uploaded_at, m.uuid, m.reason 
               FROM litebans_mute_proof p 
               LEFT JOIN litebans_mutes m ON p.mute_id = m.id";

if ($filter_proof_type !== 'all') {
    $ban_query .= " WHERE p.proof_type = '$filter_proof_type'";
    $mute_query .= " WHERE p.proof_type = '$filter_proof_type'";
}

// Получение пруфов в зависимости от фильтра
if ($filter_type === 'ban' || $filter_type === 'all') {
    $ban_proofs_result = $conn->query($ban_query . " ORDER BY p.uploaded_at DESC" . ($filter_type === 'all' ? " LIMIT $offset, $items_per_page" : ""));
    $ban_proofs = [];
    while ($proof = $ban_proofs_result->fetch_assoc()) {
        $proof['type'] = 'ban';
        $ban_proofs[] = $proof;
    }
}

if ($filter_type === 'mute' || $filter_type === 'all') {
    $mute_proofs_result = $conn->query($mute_query . " ORDER BY p.uploaded_at DESC" . ($filter_type === 'all' ? "" : " LIMIT $offset, $items_per_page"));
    $mute_proofs = [];
    while ($proof = $mute_proofs_result->fetch_assoc()) {
        $proof['type'] = 'mute';
        $mute_proofs[] = $proof;
    }
}

// Формируем итоговый список пруфов
$proofs = [];
if ($filter_type === 'ban') {
    $proofs = $ban_proofs;
} elseif ($filter_type === 'mute') {
    $proofs = $mute_proofs;
} else {
    // Если выбраны все типы, объединяем результаты и сортируем по дате
    $proofs = array_merge($ban_proofs ?? [], $mute_proofs ?? []);
    usort($proofs, function($a, $b) {
        return strtotime($b['uploaded_at']) - strtotime($a['uploaded_at']);
    });
    
    // Применяем пагинацию к объединенному результату
    $proofs = array_slice($proofs, $offset, $items_per_page);
}

// Получение общего количества пруфов для пагинации
$total_ban_proofs = $conn->query("SELECT COUNT(*) as count FROM litebans_proof" . ($filter_proof_type !== 'all' ? " WHERE proof_type = '$filter_proof_type'" : ""))->fetch_assoc()['count'];
$total_mute_proofs = $conn->query("SELECT COUNT(*) as count FROM litebans_mute_proof" . ($filter_proof_type !== 'all' ? " WHERE proof_type = '$filter_proof_type'" : ""))->fetch_assoc()['count'];

$total_proofs = ($filter_type === 'ban') ? $total_ban_proofs : (($filter_type === 'mute') ? $total_mute_proofs : ($total_ban_proofs + $total_mute_proofs));
$total_pages = ceil($total_proofs / $items_per_page);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Управление пруфами - LiteBans Админ панель</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="navbar">
        <h1>LiteBans Админ панель</h1>
        <ul>
            <li><a href="index.php">Главная</a></li>
            <li><a href="upload_proof.php">Загрузить пруфы</a></li>
            <li><a href="manage_proofs.php">Управление пруфами</a></li>
            <li><a href="logout.php">Выход</a></li>
        </ul>
    </div>

    <div class="container">
        <h2>Управление пруфами</h2>
        
        <?php if(!empty($success)): ?>
            <div class="message success-message"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <?php if(!empty($error)): ?>
            <div class="message error-message"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <div class="card">
            <div class="form-group">
                <form method="GET" action="">
                    <div style="display: flex; gap: 10px;">
                        <div>
                            <label for="filter_type">Тип наказания:</label>
                            <select id="filter_type" name="filter_type" onchange="this.form.submit()">
                                <option value="all" <?php echo $filter_type === 'all' ? 'selected' : ''; ?>>Все</option>
                                <option value="ban" <?php echo $filter_type === 'ban' ? 'selected' : ''; ?>>Баны</option>
                                <option value="mute" <?php echo $filter_type === 'mute' ? 'selected' : ''; ?>>Муты</option>
                            </select>
                        </div>
                        <div>
                            <label for="filter_proof_type">Тип пруфа:</label>
                            <select id="filter_proof_type" name="filter_proof_type" onchange="this.form.submit()">
                                <option value="all" <?php echo $filter_proof_type === 'all' ? 'selected' : ''; ?>>Все</option>
                                <option value="image" <?php echo $filter_proof_type === 'image' ? 'selected' : ''; ?>>Изображения</option>
                                <option value="video" <?php echo $filter_proof_type === 'video' ? 'selected' : ''; ?>>Видео</option>
                            </select>
                        </div>
                    </div>
                </form>
            </div>
            
            <div class="proof-container">
                <?php foreach ($proofs as $proof): ?>
                    <div class="proof-item">
                        <?php if ($proof['proof_type'] === 'image'): ?>
                            <img src="<?php echo '../' . htmlspecialchars($proof['proof_url']); ?>" alt="Пруф">
                        <?php elseif ($proof['proof_type'] === 'video'): ?>
                            <video controls>
                                <source src="<?php echo '../' . htmlspecialchars($proof['proof_url']); ?>" type="video/mp4">
                                Ваш браузер не поддерживает видео.
                            </video>
                        <?php endif; ?>
                        
                        <div class="proof-info">
                            <p>ID: <?php echo $proof['id']; ?></p>
                            <p>Тип: <?php echo $proof['type'] === 'ban' ? 'Бан' : 'Мут'; ?></p>
                            <p>ID наказания: <?php echo $proof['type'] === 'ban' ? $proof['ban_id'] : $proof['mute_id']; ?></p>
                            <p>UUID: <?php echo htmlspecialchars($proof['uuid']); ?></p>
                            <p>Дата: <?php echo $proof['uploaded_at']; ?></p>
                        </div>
                        
                        <div class="proof-actions">
                            <a href="view_proof.php?type=<?php echo $proof['type']; ?>&id=<?php echo $proof['id']; ?>" class="btn btn-primary">Просмотр</a>
                            <a href="manage_proofs.php?action=delete&type=<?php echo $proof['type']; ?>&id=<?php echo $proof['id']; ?>" class="btn btn-danger" onclick="return confirm('Вы уверены, что хотите удалить этот пруф?')">Удалить</a>
                        </div>
                    </div>
                <?php endforeach; ?>
                
                <?php if (empty($proofs)): ?>
                    <p>Пруфы не найдены.</p>
                <?php endif; ?>
            </div>
            
            <?php if ($total_pages > 1): ?>
                <div style="margin-top: 20px; text-align: center;">
                    <div class="pagination">
                        <?php if ($page > 1): ?>
                            <a href="?page=<?php echo $page - 1; ?>&filter_type=<?php echo $filter_type; ?>&filter_proof_type=<?php echo $filter_proof_type; ?>" class="btn">← Назад</a>
                        <?php endif; ?>
                        
                        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
                            <a href="?page=<?php echo $i; ?>&filter_type=<?php echo $filter_type; ?>&filter_proof_type=<?php echo $filter_proof_type; ?>" class="btn <?php echo $i === $page ? 'btn-primary' : ''; ?>"><?php echo $i; ?></a>
                        <?php endfor; ?>
                        
                        <?php if ($page < $total_pages): ?>
                            <a href="?page=<?php echo $page + 1; ?>&filter_type=<?php echo $filter_type; ?>&filter_proof_type=<?php echo $filter_proof_type; ?>" class="btn">Далее →</a>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
