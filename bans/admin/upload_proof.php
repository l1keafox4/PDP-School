<?php
include 'auth.php';
include 'db_config.php';

// Увеличиваем лимиты загрузки до 300 МБ
ini_set('upload_max_filesize', '300M');
ini_set('post_max_size', '300M');
ini_set('max_execution_time', '300');

// Директории для загрузки файлов
$upload_dir = '../uploads/';
$proofs_dir = $upload_dir . 'proofs/';

// Создаем директории, если они не существуют
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}
if (!file_exists($proofs_dir)) {
    mkdir($proofs_dir, 0755, true);
}

// Сообщения
$success = '';
$error = '';

// Получение самых свежих активных банов с именами игроков - сортировка по ID по убыванию
$activeBans = $conn->query("SELECT b.id, b.uuid, b.reason, b.time, b.banned_by_name, 
    (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name 
    FROM litebans_bans b WHERE b.active = b'1' ORDER BY b.id DESC");

$activeMutes = $conn->query("SELECT m.id, m.uuid, m.reason, m.time, m.banned_by_name, 
    (SELECT h.name FROM litebans_history h WHERE h.uuid = m.uuid ORDER BY h.date DESC LIMIT 1) AS player_name 
    FROM litebans_mutes m WHERE m.active = b'1' ORDER BY m.id DESC");

// Обработка формы
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Получаем данные из формы
    $punishment_type = isset($_POST['punishment_type']) ? $_POST['punishment_type'] : '';
    $punishment_id = isset($_POST['punishment_id']) ? $_POST['punishment_id'] : '';
    
    // Проверка для отладки - какие поля были отправлены
    error_log("Punishment ID from form: " . $punishment_id);
    
    $admin_feedback = isset($_POST['admin_feedback']) ? $_POST['admin_feedback'] : '';
    
    // Подробное логирование
    error_log("=== FORM SUBMISSION DEBUG ====");
    error_log("POST Data: " . print_r($_POST, true));
    error_log("FILES Data: " . print_r($_FILES, true));
    error_log("Punishment Type: " . $punishment_type);
    error_log("Punishment ID: " . $punishment_id);
    error_log("==========================");
    
    // Валидация данных
    if (empty($punishment_type)) {
        $error = 'Jazo turini tanlang';
    } 
    elseif (empty($punishment_id)) {
        $error = ($punishment_type === 'ban') ? 'Ban tanlang' : 'Mute tanlang';
    }
    // Проверка наличия файла
    elseif (!isset($_FILES['proof_file']) || empty($_FILES['proof_file']['name'])) {
        $error = 'Dalil faylini yuklang';
    }
    // Проверка ошибок загрузки файла
    elseif ($_FILES['proof_file']['error'] !== UPLOAD_ERR_OK) {
        $error = 'Fayl yuklashda xatolik: ' . $_FILES['proof_file']['error'];
    }
    else {
        // Обработка загрузки файла
        $file_tmp = $_FILES['proof_file']['tmp_name'];
        $file_name = $_FILES['proof_file']['name'];
        $file_size = $_FILES['proof_file']['size'];
        $file_ext = pathinfo($file_name, PATHINFO_EXTENSION);
        
        // Максимальный размер файла (300 МБ)
        $max_size = 300 * 1024 * 1024;
        
        // Проверяем расширение файла
        $allowed_ext = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'webm', 'mov', 'avi'];
        
        if ($file_size > $max_size) {
            $error = 'Fayl hajmi juda katta. Maksimal hajm - 300 MB';
        }
        elseif (!in_array(strtolower($file_ext), $allowed_ext)) {
            $error = 'Faqat rasm va video formatlar ruxsat etiladi';
        }
        else {
            // Генерируем уникальное имя для файла
            $new_file_name = uniqid() . '.' . $file_ext;
            $upload_path = $proofs_dir . $new_file_name;
            
            // Перемещаем загруженный файл
            if (move_uploaded_file($file_tmp, $upload_path)) {
                // Определяем тип доказательства (изображение или видео)
                $proof_type = in_array(strtolower($file_ext), ['jpg', 'jpeg', 'png', 'gif', 'webp']) ? 'image' : 'video';
                
                // Подготавливаем URL файла
                $proof_url = '../uploads/proofs/' . $new_file_name;
                
                try {
                    // Добавляем получение дополнительных данных для сохранения в таблицу доказательств
                    $player_name = '';
                    $admin_name = '';
                    $reason = '';
                    
                    // Получаем данные о деталях наказания в зависимости от типа
                    if ($punishment_type === 'ban') {
                        $banInfo = $conn->prepare("SELECT b.reason, b.banned_by_name, 
                            (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name 
                            FROM litebans_bans b WHERE b.id = ?");
                        $banInfo->bind_param("i", $punishment_id);
                        $banInfo->execute();
                        $banResult = $banInfo->get_result();
                        
                        if ($banRow = $banResult->fetch_assoc()) {
                            $player_name = $banRow['player_name'] ?? '';
                            $admin_name = $banRow['banned_by_name'] ?? '';
                            $reason = $banRow['reason'] ?? '';
                        }
                        $banInfo->close();
                        
                        // Для банов - используем таблицу litebans_proof c дополнительными полями
                        $sql = "INSERT INTO litebans_proof (ban_id, proof_url, proof_type, player_name, admin_name, reason, admin_feedback) VALUES (?, ?, ?, ?, ?, ?, ?)";                        
                        $stmt = $conn->prepare($sql);
                        
                        if (!$stmt) {
                            throw new Exception("SQL prepare error (ban): " . $conn->error);
                        }
                        
                        // Привязываем параметры
                        $stmt->bind_param("issssss", $punishment_id, $proof_url, $proof_type, $player_name, $admin_name, $reason, $admin_feedback);
                        error_log("Inserting into litebans_proof with extra data: ban_id=$punishment_id, player=$player_name, admin=$admin_name");
                    } 
                    else if ($punishment_type === 'mute') {
                        $muteInfo = $conn->prepare("SELECT m.reason, m.banned_by_name, 
                            (SELECT h.name FROM litebans_history h WHERE h.uuid = m.uuid ORDER BY h.date DESC LIMIT 1) AS player_name 
                            FROM litebans_mutes m WHERE m.id = ?");
                        $muteInfo->bind_param("i", $punishment_id);
                        $muteInfo->execute();
                        $muteResult = $muteInfo->get_result();
                        
                        if ($muteRow = $muteResult->fetch_assoc()) {
                            $player_name = $muteRow['player_name'] ?? '';
                            $admin_name = $muteRow['banned_by_name'] ?? '';
                            $reason = $muteRow['reason'] ?? '';
                        }
                        $muteInfo->close();
                        
                        // Для мутов - используем таблицу litebans_mute_proof с дополнительными полями
                        $sql = "INSERT INTO litebans_mute_proof (mute_id, proof_url, proof_type, player_name, admin_name, reason, admin_feedback) VALUES (?, ?, ?, ?, ?, ?, ?)";                        
                        $stmt = $conn->prepare($sql);
                        
                        if (!$stmt) {
                            throw new Exception("SQL prepare error (mute): " . $conn->error);
                        }
                        
                        // Привязываем параметры
                        $stmt->bind_param("issssss", $punishment_id, $proof_url, $proof_type, $player_name, $admin_name, $reason, $admin_feedback);
                        error_log("Inserting into litebans_mute_proof with extra data: mute_id=$punishment_id, player=$player_name, admin=$admin_name");
                    } 
                    else {
                        throw new Exception("Invalid punishment type: $punishment_type");
                    }
                    
                    // Выполняем запрос
                    if ($stmt->execute()) {
                        $success = 'Dalil muvaffaqiyatli yuklandi!';
                        
                        // Логирование успешной загрузки пруфа
                        $log_file = __DIR__ . '/../PLUGIN_DEVELOPING/ban_activity.log';
                        $timestamp = date('[Y-m-d H:i:s]');
                        $log_message = "Пруф опубликован для игрока $player_name от админа " . $_SESSION['username'];
                        
                        // Создаем директорию для логов, если не существует
                        $log_dir = dirname($log_file);
                        if (!file_exists($log_dir)) {
                            mkdir($log_dir, 0755, true);
                        }
                        
                        // Записываем в лог
                        file_put_contents($log_file, "$timestamp $log_message\n", FILE_APPEND);
                        
                        // Отправка уведомления в Telegram, если функция доступна
                        $telegram_bot_token = '7665890197:AAE89GCrTvoL1C_F0HLNJpItW--crlrt91A';
                        $telegram_chat_id = '1400003638';
                        
                        if (function_exists('curl_init')) {
                            $url = "https://api.telegram.org/bot$telegram_bot_token/sendMessage";
                            $params = [
                                'chat_id' => $telegram_chat_id,
                                'text' => "<b>🟢 ПРУФ ОПУБЛИКОВАН</b>\n\nАдминистратор <b>" . $_SESSION['username'] . "</b> опубликовал пруф для бана игрока <b>$player_name</b>.",
                                'parse_mode' => 'HTML'
                            ];
                            
                            $ch = curl_init();
                            curl_setopt($ch, CURLOPT_URL, $url);
                            curl_setopt($ch, CURLOPT_POST, true);
                            curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
                            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
                            curl_exec($ch);
                            curl_close($ch);
                        }
                        
                        // Сохраняем комментарий, если он есть
                        if (!empty($admin_feedback)) {
                            $comment_table = ($punishment_type === 'ban') ? 'litebans_bans' : 'litebans_mutes';
                            $comment_field = ($punishment_type === 'ban') ? 'ban_id' : 'mute_id';
                            
                            // Обновляем запись с комментарием
                            $commentSql = "UPDATE $comment_table SET reason = CONCAT(reason, ' [Admin izoh: ', ?, ']') WHERE id = ?";
                            $commentStmt = $conn->prepare($commentSql);
                            
                            if ($commentStmt) {
                                $commentStmt->bind_param("si", $admin_feedback, $punishment_id);
                                $commentStmt->execute();
                                $commentStmt->close();
                            }
                        }
                        
                        // Очищаем форму после успешной загрузки
                        $punishment_type = '';
                        $punishment_id = '';
                        $admin_feedback = '';
                    } else {
                        throw new Exception("SQL execute error: " . $stmt->error);
                    }
                    
                    $stmt->close();
                } catch (Exception $e) {
                    $error = 'Ma\'lumotlar bazasiga saqlashda xatolik: ' . $e->getMessage();
                    error_log("Database error: " . $e->getMessage());
                    // Удаляем загруженный файл, если не удалось сохранить в БД
                    unlink($upload_path);
                }
            } else {
                $error = 'Faylni yuklashda xatolik yuz berdi';
            }
        }
    }
}
// Ответ для AJAX-запросов
if (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest') {
    header('Content-Type: application/json');
    echo json_encode(!empty($error) ? ['error' => $error] : ['success' => $success]);
    exit;
}
?>
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dalillarni yuklash - BeastMine Admin panel</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Segoe UI', Tahoma, sans-serif;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .card {
            background-color: #252547;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .card-header {
            background-color: #16213e;
            color: #ffcc00;
            font-size: 18px;
            font-weight: bold;
            padding: 15px 20px;
            border-bottom: 1px solid #3e3e70;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #ffcc00;
        }
        
        .form-control {
            width: 100%;
            padding: 10px;
            background-color: #1e1e42;
            border: 1px solid #3e3e70;
            border-radius: 5px;
            color: #e6e6e6;
            font-size: 16px;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #ffcc00;
            box-shadow: 0 0 4px rgba(255, 204, 0, 0.6);
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background-color: #2d46b9;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #1a2d8e;
        }
        
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .alert-success {
            background-color: #1e6641;
            color: #a3ffcb;
        }
        
        .alert-danger {
            background-color: #8b2d2d;
            color: #ffc4c4;
        }
        
        .text-muted {
            color: #b0b0cc;
            font-size: 14px;
        }
        
        .punishment-selector {
            display: none;
        }
        
        /* Стили для кастомной кнопки загрузки файла */
        .custom-file-upload {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .file-label {
            background-color: #2d46b9;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 0;
            transition: background-color 0.3s;
        }
        
        .file-label:hover {
            background-color: #1a2d8e;
        }
        
        .file-name {
            color: #b0b0cc;
            font-size: 14px;
        }
        
        .file-info {
            margin-top: 5px;
            color: #ffcc00;
        }
            /* Прогресс-бар */
        .progress {
            background-color: #1e1e42;
            border: 1px solid #3e3e70;
            border-radius: 5px;
            height: 20px;
            width: 100%;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-bar {
            background-color: #2d46b9;
            height: 100%;
            width: 0%;
            transition: width 0.2s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Admin Panel - Dalillarni yuklash</h1>
        
        <?php if (!empty($success)): ?>
            <div class="alert alert-success"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <?php if (!empty($error)): ?>
            <div class="alert alert-danger"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <div class="card">
            <div class="card-header">Dalillarni yuklash</div>
            <div class="card-body">
                <!-- Форма загрузки доказательств -->
                <form method="POST" action="" enctype="multipart/form-data">
                    <!-- Выбор типа наказания -->
                    <div class="form-group">
                        <label for="punishment_type">Jazo turi:</label>
                        <select id="punishment_type" name="punishment_type" class="form-control" required>
                            <option value="">Turni tanlang</option>
                            <option value="ban" <?php echo ($punishment_type === 'ban') ? 'selected' : ''; ?>>Ban</option>
                            <option value="mute" <?php echo ($punishment_type === 'mute') ? 'selected' : ''; ?>>Mute</option>
                        </select>
                    </div>
                    
                    <!-- Скрытое поле для ID наказания -->
                    <input type="hidden" id="punishment_id" name="punishment_id" value="">
                    
                    <!-- Выбор бана -->
                    <div id="ban_selector" class="form-group punishment-selector">
                        <label for="ban_id">Ban tanlang:</label>
                        <select id="ban_id" class="form-control">
                            <option value="">Ban tanlang</option>
                            <?php while ($ban = $activeBans->fetch_assoc()): ?>
                                <?php $player_name = empty($ban['player_name']) ? $ban['uuid'] : $ban['player_name']; ?>
                                <option value="<?php echo $ban['id']; ?>">
                                    #<?php echo $ban['id']; ?> | Admin: <?php echo htmlspecialchars($ban['banned_by_name']); ?>, 

                                    O'yinchi: <?php echo htmlspecialchars($player_name); ?>
                                </option>
                            <?php endwhile; ?>
                        </select>
                    </div>
                    
                    <!-- Выбор мута -->
                    <div id="mute_selector" class="form-group punishment-selector">
                        <label for="mute_id">Mute tanlang:</label>
                        <select id="mute_id" class="form-control">
                            <option value="">Mute tanlang</option>
                            <?php while ($mute = $activeMutes->fetch_assoc()): ?>
                                <?php $player_name = empty($mute['player_name']) ? $mute['uuid'] : $mute['player_name']; ?>
                                <option value="<?php echo $mute['id']; ?>">
                                    #<?php echo $mute['id']; ?> | Admin: <?php echo htmlspecialchars($mute['banned_by_name']); ?>, 

                                    O'yinchi: <?php echo htmlspecialchars($player_name); ?>
                                </option>
                            <?php endwhile; ?>
                        </select>
                    </div>
                    
                    <!-- Загрузка файла с кастомным стилем -->
                    <div class="form-group">
                        <label for="proof_file">Dalil faylini yuklash:</label>
                        <div class="custom-file-upload">
                            <input type="file" id="proof_file" name="proof_file" class="file-input" required 
                                   accept="image/jpeg,image/png,image/gif,image/webp,video/mp4,video/webm,video/mov,video/avi" style="display: none;">
                            <label for="proof_file" class="file-label">Fayl tanlang</label>
                            <span class="file-name">Fayl tanlanmagan</span>
                        </div>
                        <small class="text-muted">Tasdiqlanadigan formatlar: JPG, PNG, GIF, WEBP, MP4, WEBM, MOV, AVI. Maksimal hajm: 300 MB</small>
                    </div>
                    
                    <!-- Прогресс-бар загрузки -->
                    <div class="form-group" id="progress_container" style="display:none;">
                        <label>Yuklash jarayoni:</label>
                        <div class="progress">
                            <div class="progress-bar" id="upload_progress_bar"></div>
                        </div>
                        <small id="progress_text" class="text-muted">0%</small>
                    </div>

                    <!-- Комментарий администратора -->
                    <!-- <div class="form-group">
                        <label for="admin_feedback">Administrator izohi (ixtiyoriy):</label>
                        <textarea id="admin_feedback" name="admin_feedback" class="form-control" rows="3" 
                                  placeholder=" dShu joydaalil haqida izoh qoldirishingiz mumkin"><?php echo htmlspecialchars($admin_feedback ?? ''); ?></textarea>
                    </div> -->
                    
                    <!-- Кнопка отправки -->
                    <div class="form-group text-center">
                        <button type="submit" class="btn btn-primary">Dalilni yuklash</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        $(document).ready(function() {
            // Функция для показа/скрытия селекторов в зависимости от типа наказания
            function updateSelectors() {
                // Получаем выбранный тип
                var type = $('#punishment_type').val();
                
                // Скрываем все селекторы
                $('.punishment-selector').hide();
                
                // Сбрасываем значение скрытого поля punishment_id
                $('#punishment_id').val('');
                
                // Показываем нужный селектор
                if (type === 'ban') {
                    $('#ban_selector').show();
                    $('#ban_id').val('');  // Сбрасываем значение селектора бана
                } else if (type === 'mute') {
                    $('#mute_selector').show();
                    $('#mute_id').val('');  // Сбрасываем значение селектора мута
                }
            }
            
            // Обработчик изменения типа наказания
            $('#punishment_type').change(updateSelectors);
            
            // Обработчик выбора бана
            $('#ban_id').change(function() {
                // Записываем выбранный ID бана в скрытое поле punishment_id
                var selectedId = $(this).val();
                $('#punishment_id').val(selectedId);
                console.log('Ban selected, punishment_id set to:', selectedId);
            });
            
            // Обработчик выбора мута
            $('#mute_id').change(function() {
                // Записываем выбранный ID мута в скрытое поле punishment_id
                var selectedId = $(this).val();
                $('#punishment_id').val(selectedId);
                console.log('Mute selected, punishment_id set to:', selectedId);
            });
            
            // Обработчик выбора файла
            $('#proof_file').change(function() {
                var file = this.files[0];
                if (file) {
                    // Обновляем текст с названием файла
                    $('.file-name').text(file.name);
                    
                    // Удаляем предыдущие сообщения
                    $('.file-info').remove();
                    
                    // Добавляем информацию о файле
                    var fileInfo = $('<div class="file-info"></div>');
                    fileInfo.text('Hajmi: ' + Math.round(file.size / 1024) + ' KB');
                    $('.custom-file-upload').append(fileInfo);
                }
            });
            
            // Запускаем при загрузке страницы
            updateSelectors();
            
            // Валидация и AJAX-отправка с прогресс-баром
            $('form').on('submit', function(e) {
                e.preventDefault(); // остановить стандартную отправку
                // Получаем тип наказания
                var type = $('#punishment_type').val();
                
                // Создаем запись в консоли
                console.log('Submitting form with the following data:');
                console.log('Type:', type);
                
                // Проверяем выбор типа наказания
                if (!type) {
                    alert('Iltimos, jazo turini tanlang!');
                    e.preventDefault();
                    return false;
                }
                
                // Проверяем выбор наказания в зависимости от типа
                if (type === 'ban') {
                    var banId = $('#ban_id').val();
                    console.log('Ban ID:', banId);
                    
                    if (!banId) {
                        alert('Iltimos, ban tanlang!');
                        e.preventDefault();
                        return false;
                    }
                } else if (type === 'mute') {
                    var muteId = $('#mute_id').val();
                    console.log('Mute ID:', muteId);
                    
                    if (!muteId) {
                        alert('Iltimos, mute tanlang!');
                        e.preventDefault();
                        return false;
                    }
                }
                
                // Проверяем выбор файла
                var fileSelected = $('#proof_file').val();
                console.log('File selected:', fileSelected ? 'Yes' : 'No');
                
                if (!fileSelected) {
                    alert('Iltimos, dalil faylini yuklang!');
                    e.preventDefault();
                    return false;
                }
                
                // Все проверки пройдены – отправляем через AJAX с отображением прогресса
                var formElement = this;
                var formData = new FormData(formElement);

                // показать прогресс-бар
                $('#progress_container').show();
                $('#upload_progress_bar').css('width', '0%');
                $('#progress_text').text('0%');

                $.ajax({
                    url: $(formElement).attr('action') || '',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    xhr: function () {
                        var xhr = $.ajaxSettings.xhr();
                        if (xhr.upload) {
                            xhr.upload.addEventListener('progress', function (event) {
                                if (event.lengthComputable) {
                                    var percent = Math.round((event.loaded / event.total) * 100);
                                    $('#upload_progress_bar').css('width', percent + '%');
                                    $('#progress_text').text(percent + '%');
                                }
                            }, false);
                        }
                        return xhr;
                    },
                    success: function (res) {
                        try {
                            var json = (typeof res === 'string') ? JSON.parse(res) : res;
                            if (json.error) {
                                alert(json.error);
                            } else {
                                alert(json.success || 'Yuklash muvaffaqiyatli!');
                                location.reload();
                            }
                        } catch (e) {
                            location.reload();
                        }
                    },
                    error: function () {
                        alert('Yuklash vaqtida xatolik yuz berdi');
                    }
                });

                return false;
            });
        });
    </script>
</body>
</html>
