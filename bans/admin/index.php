<?php
include 'auth.php';
include 'db_config.php';

// Получение статистики
$banCount = $conn->query("SELECT COUNT(*) as count FROM litebans_bans")->fetch_assoc()['count'];
$muteCount = $conn->query("SELECT COUNT(*) as count FROM litebans_mutes")->fetch_assoc()['count'];
$banProofCount = $conn->query("SELECT COUNT(*) as count FROM litebans_proof")->fetch_assoc()['count'];
$muteProofCount = $conn->query("SELECT COUNT(*) as count FROM litebans_mute_proof")->fetch_assoc()['count'];
?>
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeastMine Admin panel</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="modern.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Segoe UI', Tahoma, sans-serif;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .navbar {
            background-color: #222461;
            border-bottom: 3px solid #ffcc00;
        }
        
        .card {
            background-color: #2a2a4a;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .card-header {
            background-color: #292954;
            padding: 15px 20px;
            border-bottom: 1px solid #393963;
            font-weight: bold;
            font-size: 18px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 15px;
        }
        
        .stat-card {
            background-color: #222461;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .stat-number {
            font-size: 32px;
            font-weight: bold;
            color: #ffcc00;
            margin: 10px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background-color: #292954;
            padding: 12px 15px;
            text-align: left;
            font-weight: bold;
            color: #e6e6e6;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #393963;
        }
        
        tr:hover {
            background-color: #222461;
        }
        
        .btn {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background-color: #ffcc00;
            color: #222;
        }
        
        .btn-primary:hover {
            background-color: #e6b800;
        }
        
        .tabs-container {
            margin-bottom: 20px;
        }
        
        .tabs {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #292954;
            border-radius: 12px 12px 0 0;
        }
        
        .tab {
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            color: #e6e6e6;
            text-decoration: none;
            transition: all 0.2s;
        }
        
        .tab.active {
            background-color: #222461;
            border-radius: 12px 12px 0 0;
        }
        
        .tabs-left {
            display: flex;
            align-items: center;
        }
        
        .tabs-right {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            flex: 1;
        }
        
        #sticky-tabs {
            position: sticky;
            top: 0;
            z-index: 1;
        }
        
        #sticky-tabs.sticky {
            background-color: #1a1a2e;
            padding: 10px;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .square-id {
            display: inline-block;
            width: 40px;
            height: 40px;
            background-color: #ffcc00;
            color: #222;
            font-weight: bold;
            font-size: 18px;
            text-align: center;
            line-height: 40px;
            border-radius: 10px;
        }
        
        .player-info {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .player-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .ban-id, .mute-id {
            font-size: 14px;
            color: #999;
            margin-bottom: 5px;
        }
        
        /* Удаляем эти стили, чтобы использовать стили из modern.css */
        /*
        .ban-reason, .mute-reason {
            font-size: 14px;
            color: #666;
        }
        */
        
        .inline-id {
            font-size: 14px;
            color: #999;
            margin-left: 5px;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>BeastMine Admin panel</h1>
        <ul>
            <li><a href="index.php">Asosiy</a></li>
            <li><a href="upload_proof.php">Dalillarni yuklash</a></li>
            <?php if(isset($_SESSION['role']) && $_SESSION['role']==='admin'): ?>
            <li><a href="my_helper.php">Mening yordamchim</a></li>
            <?php endif; ?>
            <?php if(isset($_SESSION['role']) && $_SESSION['role']==='owner'): ?>
            <li><a href="manage_helpers.php">Yordamchilarni boshqarish</a></li>
            <?php endif; ?>
            <li><a href="logout.php">Chiqish</a></li>
        </ul>
    </div>

    <div class="container">
        <h2>Xush kelibsiz, <?php echo htmlspecialchars($_SESSION['username']); ?>!</h2>
        
        <div class="card">
            <div class="card-header">Statistika</div>
            <div class="card-body">
                <div class="stats-grid">
                    <div class="stat-card">
                        <h4>Barcha banlar</h4>
                        <div class="stat-number"><?php echo $banCount; ?></div>
                    </div>
                    <div class="stat-card">
                        <h4>Barcha mutelar</h4>
                        <div class="stat-number"><?php echo $muteCount; ?></div>
                    </div>
                    <div class="stat-card">
                        <h4>Ban dalillari</h4>
                        <div class="stat-number"><?php echo $banProofCount; ?></div>
                    </div>
                    <div class="stat-card">
                        <h4>Mute dalillari</h4>
                        <div class="stat-number"><?php echo $muteProofCount; ?></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                So'nggi qo'shilgan ro'yxatlar
            </div>
            
            <div class="tabs-container" id="sticky-tabs">
                <div class="tabs">
                    <div class="tabs-left">
                        <a href="index.php?section=banlar" class="tab <?php echo (!isset($_GET['section']) || $_GET['section'] === 'banlar') ? 'active' : ''; ?>">Banlar</a>
                        <a href="index.php?section=mutelar" class="tab <?php echo (isset($_GET['section']) && $_GET['section'] === 'mutelar') ? 'active' : ''; ?>">Mutelar</a>
                    </div>
                    <div class="tabs-right">
                        <button id="refreshDataBtn" class="refresh-btn" title="Yangilash">
                            <i class="material-icons">refresh</i>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="card-body">
                <div id="dalillarLoading" style="display: none; text-align: center; padding: 20px;">
                    <div class="loading"></div>
                    <p>Ma'lumotlar yuklanmoqda...</p>
                </div>
                <div id="dalillarContainer">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Turi</th>
                                <th>Jazo ID</th>
                                <th>Dalil turi</th>
                                <th>Qo'shilgan sana</th>
                                <th>Amallar</th>
                            </tr>
                        </thead>
                        <tbody id="dalillarBody">
                            <?php
                            // Отладочный вывод ошибок SQL
                            mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
                            
                            $section = isset($_GET['section']) ? $_GET['section'] : 'banlar';
                            $hasProofs = false;
                            
                            if ($section === 'mutelar') {
                                // Получение последних пруфов для мутов с именами игроков
                                $muteProofsQuery = "SELECT p.id, p.mute_id, p.proof_type, p.proof_url, UNIX_TIMESTAMP() as timestamp_now, m.banned_by_name, 
                                    (SELECT h.name FROM litebans_history h WHERE h.uuid = m.uuid ORDER BY h.date DESC LIMIT 1) AS player_name,
                                    m.reason
                                    FROM litebans_mute_proof p 
                                    JOIN litebans_mutes m ON p.mute_id = m.id
                                    ORDER BY p.id DESC LIMIT 20";
                                    
                                try {
                                    $muteProofs = $conn->query($muteProofsQuery);
                                    
                                    while ($proof = $muteProofs->fetch_assoc()) {
                                        $hasProofs = true;
                                        $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['mute_id'] : $proof['player_name'];
                                        $proof_type_text = $proof['proof_type'] == 'image' ? 'Rasm' : 'Video';
                                        $proof_type_class = $proof['proof_type'] == 'image' ? 'badge-image' : 'badge-video';
                                        $reason = !empty($proof['reason']) ? htmlspecialchars($proof['reason']) : "Chat qoidalarini buzganlik uchun";
                                        
                                        // Используем регулярное выражение для извлечения текста причины
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
                                        
                                        echo "<tr class='data-row'>";
                                        echo "<td><div class='square-id'>" . $proof['id'] . "</div></td>";
                                        echo "<td><span class='badge badge-mute'>Mute</span></td>";
                                        echo "<td>
                                            <div class='player-info'>
                                                <div class='player-name'>" . htmlspecialchars($player_name) . " <span class='inline-id'>#" . $proof['mute_id'] . "</span></div>
                                                <div class='mute-reason'>" . $reason . "</div>
                                            </div>
                                        </td>";
                                        echo "<td><span class='badge {$proof_type_class}'>" . $proof_type_text . "</span></td>";
                                        echo "<td>" . date('Y-m-d H:i:s', $proof['timestamp_now']) . "</td>";
                                        echo "<td><a href='javascript:void(0)' onclick='showProofModal(\"" . htmlspecialchars($proof['proof_url']) . "\", \"mute\", \"" . $proof['proof_type'] . "\", \"" . $proof['id'] . "\")' class='btn btn-primary btn-view'><i class='material-icons' style='font-size: 16px;'>visibility</i> Ko'rish</a></td>";
                                        echo "</tr>";
                                    }
                                    
                                } catch (Exception $e) {
                                    echo "<tr><td colspan='6'><div class='empty-state'><i class='material-icons'>error</i>Ошибка запроса мутов: " . $e->getMessage() . "</div></td></tr>";
                                    $muteProofs = null;
                                }
                                
                            } else {
                                // Получение последних пруфов для банов с именами игроков
                                $banProofsQuery = "SELECT p.id, p.ban_id, p.proof_type, p.proof_url, UNIX_TIMESTAMP() as timestamp_now, b.banned_by_name, 
                                    (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name,
                                    b.reason
                                    FROM litebans_proof p 
                                    JOIN litebans_bans b ON p.ban_id = b.id
                                    ORDER BY p.id DESC LIMIT 20";
                                    
                                try {
                                    $banProofs = $conn->query($banProofsQuery);
                                
                                    while ($proof = $banProofs->fetch_assoc()) {
                                        $hasProofs = true;
                                        $player_name = empty($proof['player_name']) ? 'ID: ' . $proof['ban_id'] : $proof['player_name'];
                                        $proof_type_text = $proof['proof_type'] == 'image' ? 'Rasm' : 'Video';
                                        $proof_type_class = $proof['proof_type'] == 'image' ? 'badge-image' : 'badge-video';
                                        $reason = !empty($proof['reason']) ? htmlspecialchars($proof['reason']) : "Qoidani buzganlik uchun";
                                        
                                        // Используем регулярное выражение для извлечения текста причины
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
                                        
                                        echo "<tr class='data-row'>";
                                        echo "<td><div class='square-id'>" . $proof['id'] . "</div></td>";
                                        echo "<td><span class='badge badge-ban'>Ban</span></td>";
                                        echo "<td>
                                            <div class='player-info'>
                                                <div class='player-name'>" . htmlspecialchars($player_name) . " <span class='inline-id'>#" . $proof['ban_id'] . "</span></div>
                                                <div class='ban-reason'>" . $reason . "</div>
                                            </div>
                                        </td>";
                                        echo "<td><span class='badge {$proof_type_class}'>" . $proof_type_text . "</span></td>";
                                        echo "<td>" . date('Y-m-d H:i:s', $proof['timestamp_now']) . "</td>";
                                        echo "<td>
                                            <div class='btn-group'>
                                                <a href='javascript:void(0)' onclick='showProofModal(\"" . htmlspecialchars($proof['proof_url']) . "\", \"ban\", \"" . $proof['proof_type'] . "\", \"" . $proof['id'] . "\")' class='btn btn-primary btn-view'><i class='material-icons' style='font-size: 16px;'>visibility</i> Ko'rish</a>
                                                <a href='javascript:void(0)' onclick='showUnbanModal(\"" . htmlspecialchars($proof['player_name']) . "\")' class='btn btn-success'><i class='material-icons' style='font-size: 16px;'>lock_open</i> Unban</a>
                                            </div>
                                        </td>";
                                        echo "</tr>";
                                    }
                                    
                                } catch (Exception $e) {
                                    echo "<tr><td colspan='6'><div class='empty-state'><i class='material-icons'>error</i>Ошибка запроса банов: " . $e->getMessage() . "</div></td></tr>";
                                    $banProofs = null;
                                }
                            }
                            
                            if (!$hasProofs) {
                                echo "<tr><td colspan='6'><div class='empty-state'><i class='material-icons'>info</i>Hozircha dalillar yo'q</div></td></tr>";
                            }
                            ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <!-- JavaScript для обновления данных без перезагрузки страницы -->
    <script>
    // Глобальные переменные для бесконечного скролла
    let offset = 20; // Начальное смещение (первые 20 уже загружены)
    let loading = false; // Флаг для предотвращения множественных запросов
    let hasMoreData = true; // Флаг наличия дополнительных данных
    
    // Функция для показа модального окна с доказательствами
    function showProofModal(proofUrl, type, proofType, proofId) {
        // Получаем модальное окно
        var modal = document.getElementById('proofModal');
        var modalContent = document.getElementById('proofModalContent');
        
        // Заполняем информацию в модальном окне
        document.getElementById('modalTitle').textContent = type === 'ban' ? 'Доказательство бана' : 'Доказательство мута';
        document.getElementById('proofType').textContent = proofType === 'image' ? 'Rasm' : 'Video';
        document.getElementById('proofId').textContent = proofId;
        
        // Скрываем все блоки с контентом
        document.getElementById('imageProof').style.display = 'none';
        document.getElementById('videoProof').style.display = 'none';
        document.getElementById('urlProof').style.display = 'none';
        
        // Показываем соответствующий блок в зависимости от типа доказательства
        if (proofType === 'image') {
            document.getElementById('imageProof').style.display = 'block';
            document.getElementById('proofImage').src = proofUrl;
        } else if (proofType === 'video') {
            document.getElementById('videoProof').style.display = 'block';
            document.getElementById('videoSource').src = proofUrl;
            document.getElementById('proofVideo').load(); // Загружаем видео
        } else {
            // Если тип не известен или это ссылка
            document.getElementById('urlProof').style.display = 'block';
            document.getElementById('proofUrl').href = proofUrl;
        }
        
        // Показываем модальное окно
        document.getElementById('proofModal').style.display = 'block';
        
        // Добавляем эффект появления
        setTimeout(function() {
            document.querySelector('.modal-content').classList.add('show');
        }, 10);
    }
    
    // Функция для показа модального окна разбана
    function showUnbanModal(playerName) {
        document.getElementById('unbanPlayerName').value = playerName;
        document.getElementById('unbanModalTitle').textContent = `Unban игрока ${playerName}`;
        document.getElementById('unbanReason').value = ''; // Очистка предыдущего значения
        
        // Открываем модальное окно
        var modal = document.getElementById('unbanModal');
        modal.style.display = 'flex';
        
        // Добавляем эффект появления
        setTimeout(function() {
            modal.querySelector('.modal-content').classList.add('show');
        }, 10);
    }
    
    // Функция для закрытия модального окна разбана
    function closeUnbanModal() {
        var modal = document.getElementById('unbanModal');
        modal.querySelector('.modal-content').classList.remove('show');
        setTimeout(function() {
            modal.style.display = 'none';
        }, 300);
    }
    
    // Функция для отправки запроса на разбан
    function sendUnbanRequest(playerName, reason) {
        // Показываем индикатор загрузки
        var confirmBtn = document.getElementById('confirmUnban');
        var originalText = confirmBtn.textContent;
        confirmBtn.innerHTML = '<span class="loading" style="width: 15px; height: 15px; margin-right: 5px;"></span> Отправка...';
        
        console.log('Отправка запроса на разбан для игрока:', playerName, 'Причина:', reason);
        
        // Отправляем запрос на разбан через PHP-скрипт
        fetch('/bans/admin/unban_player.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'player=' + encodeURIComponent(playerName) + '&reason=' + encodeURIComponent(reason)
        })
        .then(response => {
            console.log('Получен ответ от сервера. Статус:', response.status);
            
            // Проверяем, есть ли содержимое в ответе
            if (response.status === 204) {
                // Если статус 204, это успешный ответ без содержимого
                return { status: 'success', message: 'Игрок ' + playerName + ' успешно разбанен!' };
            }
            
            // Пытаемся распарсить JSON
            return response.json().catch(() => {
                // Если не удалось распарсить JSON, проверяем HTTP статус
                if (response.ok) {
                    // Если статус 2xx, считаем операцию успешной
                    return { status: 'success', message: 'Игрок ' + playerName + ' успешно разбанен!' };
                } else {
                    // Иначе возвращаем ошибку
                    return { status: 'error', message: 'Некорректный ответ от сервера (HTTP ' + response.status + ')' };
                }
            });
        })
        .then(data => {
            console.log('Обработанный ответ:', data);
            
            // Закрываем модальное окно
            closeUnbanModal();
            
            // Показываем уведомление о результате
            var notification = document.createElement('div');
            notification.className = 'notification ' + (data.status === 'success' ? 'success' : 'error');
            notification.textContent = data.message || 'Операция выполнена';
            document.body.appendChild(notification);
            
            // Автоматически убираем уведомление через 5 секунд
            setTimeout(function() {
                notification.classList.add('fadeOut');
                setTimeout(function() {
                    document.body.removeChild(notification);
                }, 500);
            }, 5000);
            
            // Обновляем список банов, если разбан был успешным
            if (data.status === 'success') {
                refreshData();
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
            
            // Показываем уведомление об ошибке
            var notification = document.createElement('div');
            notification.className = 'notification error';
            notification.textContent = 'Произошла ошибка при отправке запроса: ' + error.message;
            document.body.appendChild(notification);
            
            // Автоматически убираем уведомление через 5 секунд
            setTimeout(function() {
                notification.classList.add('fadeOut');
                setTimeout(function() {
                    document.body.removeChild(notification);
                }, 500);
            }, 5000);
        })
        .finally(() => {
            // Восстанавливаем текст кнопки
            confirmBtn.innerHTML = originalText;
        });
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        // Находим кнопку обновления и добавляем обработчик события
        const refreshBtn = document.getElementById('refreshDataBtn');
        const dalillarContainer = document.getElementById('dalillarContainer');
        const loadingIndicator = document.getElementById('dalillarLoading');
        
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                // Показываем индикатор загрузки
                dalillarContainer.style.display = 'none';
                loadingIndicator.style.display = 'block';
                
                // Создаем AJAX запрос для обновления данных
                const xhr = new XMLHttpRequest();
                const section = new URLSearchParams(window.location.search).get('section') || 'banlar';
                xhr.open('GET', 'index.php?section=' + section + '&refresh=1', true);
                
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        // Небольшая задержка для демонстрации анимации загрузки
                        setTimeout(function() {
                            // Скрываем индикатор загрузки
                            loadingIndicator.style.display = 'none';
                            dalillarContainer.style.display = 'block';
                            
                            // Применяем анимацию к каждой строке таблицы
                            const rows = document.querySelectorAll('.data-row');
                            rows.forEach((row, index) => {
                                row.style.animation = 'none';
                                row.offsetHeight; // Trigger reflow
                                row.style.animation = `fadeIn 0.3s ease forwards ${index * 0.1}s`;
                            });
                            
                            // Обновляем страницу
                            location.reload();
                        }, 800);
                    }
                };
                
                xhr.send();
            });
        }
        
        // Автоматическое обновление при загрузке страницы и переключении вкладок
        const navLinks = document.querySelectorAll('.navbar a');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (this.getAttribute('href').includes('section=')) {
                    // Добавляем класс active только для вкладок разделов
                    navLinks.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                    
                    if (!e.ctrlKey && !e.metaKey) { // Если не открывается в новой вкладке
                        e.preventDefault();
                        
                        // Показываем загрузку
                        dalillarContainer.style.display = 'none';
                        loadingIndicator.style.display = 'block';
                        
                        // Обновляем URL без перезагрузки страницы
                        const newUrl = this.getAttribute('href');
                        history.pushState(null, '', newUrl);
                        
                        // Загружаем новые данные через AJAX
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', newUrl, true);
                        xhr.onload = function() {
                            if (xhr.status === 200) {
                                setTimeout(function() {
                                    location.reload(); // Перезагружаем для простоты
                                }, 300);
                            }
                        };
                        xhr.send();
                    }
                }
            });
        });
        
        // Применяем анимацию появления к строкам таблицы при загрузке страницы
        const rows = document.querySelectorAll('.data-row');
        rows.forEach((row, index) => {
            row.style.animation = `fadeIn 0.3s ease forwards ${index * 0.1}s`;
            row.style.opacity = '0';
        });
        
        // Функция для определения, достиг ли пользователь конца страницы
        function isAtBottom() {
            return window.innerHeight + window.scrollY >= document.body.offsetHeight - 300;
        }
        
        // Функция загрузки дополнительных пруфов
        function loadMoreProofs() {
            if (loading || !hasMoreData) return;
            
            loading = true;
            document.getElementById('dalillarLoading').style.display = 'block';
            console.log('Loading more proofs, offset:', offset); // Отладочная информация
            
            // Получаем текущий активный раздел
            const section = '<?php echo $section; ?>';
            
            // Делаем AJAX запрос для получения новых данных
            const url = `load_more_proofs.php?section=${section}&offset=${offset}`;
            console.log('Fetching URL:', url);
            
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Received data:', data.length, 'items'); // Отладочная информация
                    // Если нет больше данных, отмечаем это
                    if (data.length === 0) {
                        hasMoreData = false;
                        document.getElementById('dalillarLoading').style.display = 'none';
                        return;
                    }
                    
                    // Добавляем новые строки в таблицу
                    const tableBody = document.getElementById('dalillarBody');
                    data.forEach(proof => {
                        const row = document.createElement('tr');
                        row.className = 'data-row';
                        
                        // Формируем HTML содержимое строки в зависимости от типа
                        const proofType = section === 'banlar' ? 'ban' : 'mute';
                        const proofTypeDisplay = section === 'banlar' ? 'Ban' : 'Mute';
                        const proofIdField = section === 'banlar' ? 'ban_id' : 'mute_id';
                        
                        row.innerHTML = `
                            <td><div class='square-id'>${proof.id}</div></td>
                            <td><span class='badge badge-${proofType}'>${proofTypeDisplay}</span></td>
                            <td>
                                <div class='player-info'>
                                    <div class='player-name'>${proof.player_name} <span class='inline-id'>#${proof[proofIdField]}</span></div>
                                    <div class='${proofType}-reason'>${proof.reason}</div>
                                </div>
                            </td>
                            <td><span class='badge badge-${proof.proof_type === 'image' ? 'image' : 'video'}'>${proof.proof_type === 'image' ? 'Rasm' : 'Video'}</span></td>
                            <td>${proof.timestamp}</td>
                            <td>
                                <div class='btn-group'>
                                    <a href='javascript:void(0)' onclick='showProofModal("${proof.proof_url}", "${proofType}", "${proof.proof_type}", "${proof.id}")' class='btn btn-primary btn-view'><i class='material-icons' style='font-size: 16px;'>visibility</i> Ko'rish</a>
                                    ${proofType === 'ban' ? `<a href='javascript:void(0)' onclick='showUnbanModal("${proof.player_name}")' class='btn btn-success'><i class='material-icons' style='font-size: 16px;'>lock_open</i> Unban</a>` : ''}
                                </div>
                            </td>
                        `;
                        
                        tableBody.appendChild(row);
                    });
                    
                    // Увеличиваем смещение для следующего запроса
                    offset += data.length;
                    loading = false;
                    document.getElementById('dalillarLoading').style.display = 'none';
                })
                .catch(error => {
                    console.error('Ошибка при загрузке данных:', error);
                    loading = false;
                    document.getElementById('dalillarLoading').style.display = 'none';
                });
        }
        
        // Обработчик скролла для бесконечной подгрузки
        window.addEventListener('scroll', function() {
            console.log('Scrolling', window.innerHeight, window.scrollY, document.body.offsetHeight);
            if (isAtBottom()) {
                console.log('At bottom, loading more proofs');
                loadMoreProofs();
            }
        });
        
        // Также добавляем обработчик на кнопку загрузки еще
        const loadMoreButton = document.createElement('button');
        loadMoreButton.textContent = 'Yana yuklash';
        loadMoreButton.className = 'btn btn-primary load-more-btn';
        loadMoreButton.style.margin = '20px auto';
        loadMoreButton.style.display = 'block';
        loadMoreButton.style.padding = '10px 20px';
        loadMoreButton.style.fontSize = '16px';
        loadMoreButton.addEventListener('click', function() {
            console.log('Load more button clicked');
            loadMoreProofs();
        });
        
        // Добавляем кнопку в конец таблицы
        document.getElementById('dalillarContainer').appendChild(loadMoreButton);
        
        // Обработчики событий для закрытия модального окна
        document.querySelector('.close').addEventListener('click', function() {
            closeProofModal();
        });
        
        document.getElementById('closeModal').addEventListener('click', function() {
            closeProofModal();
        });
        
        // Закрытие модального окна при клике вне его
        window.addEventListener('click', function(event) {
            if (event.target === document.getElementById('proofModal')) {
                closeProofModal();
            }
        });
        
        // Функция закрытия модального окна
        function closeProofModal() {
            document.querySelector('.modal-content').classList.remove('show');
            setTimeout(function() {
                document.getElementById('proofModal').style.display = 'none';
                // Очищаем содержимое видео, чтобы оно не продолжало воспроизводиться
                document.getElementById('videoSource').src = '';
                document.getElementById('proofVideo').load();
            }, 300);
        }
        
        // Обработчики для кнопок модального окна разбана
        document.getElementById('cancelUnban').addEventListener('click', function() {
            closeUnbanModal();
        });
        
        document.getElementById('closeUnbanModal').addEventListener('click', function() {
            closeUnbanModal();
        });
        
        document.getElementById('confirmUnban').addEventListener('click', function() {
            var playerName = document.getElementById('unbanPlayerName').value;
            var reason = document.getElementById('unbanReason').value.trim();
            
            if (!reason) {
                alert('Пожалуйста, укажите причину разбана');
                return;
            }
            
            sendUnbanRequest(playerName, reason);
        });
        
        // Закрытие при клике вне модального окна
        window.addEventListener('click', function(event) {
            if (event.target === document.getElementById('unbanModal')) {
                closeUnbanModal();
            }
        });
    });
    </script>
    
    <!-- Модальное окно для просмотра доказательств -->
    <div id="proofModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Просмотр доказательства</h2>
                <span class="close">&times;</span>
            </div>
            <div class="modal-body">
                <div class="proof-info">
                    <p><strong>Тип:</strong> <span id="proofType"></span></p>
                    <p><strong>ID:</strong> <span id="proofId"></span></p>
                </div>
                <div class="proof-content">
                    <div id="imageProof" style="display: none;">
                        <img id="proofImage" src="" alt="Доказательство" style="max-width: 100%; max-height: 500px;">
                    </div>
                    <div id="videoProof" style="display: none;">
                        <video id="proofVideo" controls style="max-width: 100%; max-height: 500px;">
                            <source id="videoSource" src="" type="video/mp4">
                            Ваш браузер не поддерживает видео.
                        </video>
                    </div>
                    <div id="urlProof" style="display: none;">
                        <a id="proofUrl" href="" target="_blank" class="btn btn-primary">Открыть ссылку на доказательство</a>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button id="closeModal" class="btn btn-primary">Закрыть</button>
            </div>
        </div>
    </div>
    
    <!-- Модальное окно для разбана -->
    <div id="unbanModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="unbanModalTitle">Unban игрока</h2>
                <span class="close" id="closeUnbanModal">&times;</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label for="unbanReason">Причина разбана:</label>
                    <textarea id="unbanReason" class="form-control" rows="4" placeholder="Введите причину разбана..."></textarea>
                </div>
                <input type="hidden" id="unbanPlayerName" value="">
            </div>
            <div class="modal-footer">
                <button id="cancelUnban" class="btn">Отмена</button>
                <button id="confirmUnban" class="btn btn-success">Разбанить</button>
            </div>
        </div>
    </div>
<?php if(isset($_SESSION['role'])): ?>
<script>
setInterval(()=>{ fetch('api/check_warns.php').catch(()=>{}); }, 10000);
</script>
<?php endif; ?>
</body>
</html>
