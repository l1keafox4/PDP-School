<?php
include 'auth.php';
include 'db_config.php';
// Ensure connection collation unified
$conn->query("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci");

// Check if user is owner
if ($_SESSION['role'] !== 'owner') {
    echo "<div class='error-message'>Доступ только для владельца (owner)</div>";
    header("Refresh: 3; URL=index.php");
    exit;
}

// Messages
$message = '';
$success = '';
$error = '';
$generated_password = ''; // держим пароль для вывода

// Ensure plain_password column exists
$columnCheck = $conn->query("SHOW COLUMNS FROM litebans_users LIKE 'plain_password'");
if ($columnCheck && $columnCheck->num_rows === 0) {
    $conn->query("ALTER TABLE litebans_users ADD plain_password VARCHAR(255) NULL AFTER password");
}
// Ensure parent_username column exists (guardian for helpers)
$parentCheck = $conn->query("SHOW COLUMNS FROM litebans_users LIKE 'parent_username'");
if ($parentCheck && $parentCheck->num_rows === 0) {
    $conn->query("ALTER TABLE litebans_users ADD parent_username VARCHAR(255) NULL AFTER role");
}

// Ensure helper tables exist for warns & logs
$conn->query("CREATE TABLE IF NOT EXISTS staff_warns (
    staff_username VARCHAR(128) PRIMARY KEY,
    role ENUM('admin','mod','helper') NOT NULL,
    warn_count INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");

$conn->query("CREATE TABLE IF NOT EXISTS staff_actions_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_username VARCHAR(128),
    staff_role ENUM('admin','mod','helper'),
    action VARCHAR(255),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");

// Ensure created_at column exists for ordering helpers
$createdCheck = $conn->query("SHOW COLUMNS FROM litebans_users LIKE 'created_at'");
if($createdCheck && $createdCheck->num_rows===0){
    // place after parent_username if exists, else after role
    $afterColumn = ($parentCheck && $parentCheck->num_rows===0) ? 'role' : 'parent_username';
    $conn->query("ALTER TABLE litebans_users ADD created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER $afterColumn");
}
if ($parentCheck && $parentCheck->num_rows === 0) {
    $conn->query("ALTER TABLE litebans_users ADD parent_username VARCHAR(255) NULL AFTER role");
}
// Ensure helper_passwords table exists for storing historical passwords
$conn->query("CREATE TABLE IF NOT EXISTS helper_passwords (
    username VARCHAR(255) PRIMARY KEY,
    plain_password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");

// Preload list of admin usernames for guardian dropdown & validation
$adminUsernames = [];
$adminsRes = $conn->query("SELECT username FROM litebans_users WHERE role='admin' ORDER BY username");
if($adminsRes){
    while($row=$adminsRes->fetch_assoc()){ $adminUsernames[] = $row['username']; }
    // Админы, которые уже являются опекунами
    $guardiansTaken = [];
    $resTaken = $conn->query("SELECT parent_username FROM litebans_users WHERE role='helper' AND parent_username IS NOT NULL AND parent_username != ''");
    if($resTaken){
        while($r=$resTaken->fetch_assoc()){ $guardiansTaken[] = $r['parent_username']; }
    }
}

// Add helper form processing
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    // Обновление ранга по AJAX
    if ($_POST['action'] === 'update_role' && isset($_POST['id'], $_POST['role'])) {
        $id = intval($_POST['id']);
        $role = $_POST['role'];
        $allowed_roles = ['owner','investor','admin','mod','helper'];
        header('Content-Type: application/json');
        if (in_array($role, $allowed_roles)) {
            // Check limit 5 per role (excluding this user)
            $cntStmt = $conn->prepare("SELECT COUNT(*) as c FROM litebans_users WHERE role=? AND id!=?");
            $cntStmt->bind_param("si", $role, $id);
            $cntStmt->execute();
            $cnt = $cntStmt->get_result()->fetch_assoc()['c'];
            if($cnt >= 5){
                echo json_encode(['success'=>false,'message'=>'limit']);
                exit;
            }
            $upd = $conn->prepare("UPDATE litebans_users SET role=? WHERE id=?");
            $upd->bind_param("si", $role, $id);
            $upd->execute();
            echo json_encode(['success'=>true]);
        } else {
            echo json_encode(['success'=>false]);
        }
        exit;

        exit; // возвращаем пустой ответ
    }
    // Обновление опекуна (parent)
    if ($_POST['action'] === 'update_parent' && isset($_POST['id'], $_POST['parent'])) {
        $id = intval($_POST['id']);
        $parent = trim($_POST['parent']); // может быть пустым

        // Если пусто – снимаем опекуна
        if ($parent === '') {
            $upd = $conn->prepare("UPDATE litebans_users SET parent_username=NULL WHERE id=?");
            $upd->bind_param("i", $id);
            $upd->execute();
            echo json_encode(['success' => true]);
            exit;
        }

        // Разрешаем опекуном только существующего админа
        if (!in_array($parent, $adminUsernames)) {
            echo json_encode(['success' => false, 'message' => 'invalid']);
            exit;
        }

        // Проверяем, что этот админ ещё не привязан к другому помощнику
        $existsStmt = $conn->prepare("SELECT id FROM litebans_users WHERE role='helper' AND parent_username=? AND id!=? LIMIT 1");
        $existsStmt->bind_param("si", $parent, $id);
        $existsStmt->execute();
        if ($existsStmt->get_result()->num_rows > 0) {
            echo json_encode(['success' => false, 'message' => 'occupied']);
            exit;
        }

        // Обновляем запись
        $upd = $conn->prepare("UPDATE litebans_users SET parent_username=? WHERE id=?");
        $upd->bind_param("si", $parent, $id);
        $upd->execute();
        echo json_encode(['success' => true]);
        exit;
    }
    if ($_POST['action'] === 'add') {
        $username = $_POST['username'] ?? '';
        // Получаем выбранный ранг
        $role = $_POST['role'] ?? 'helper';
        $allowed_roles = ['owner','investor','admin','mod','helper'];
        if (!in_array($role, $allowed_roles)) { $role = 'helper'; }

        // Определяем пароль: если ранее помощник уже существовал, используем его прежний пароль
        $storedPassStmt = $conn->prepare("SELECT plain_password FROM helper_passwords WHERE username=?");
        $storedPassStmt->bind_param("s", $username);
        $storedPassStmt->execute();
        $storedRes = $storedPassStmt->get_result();
        if ($storedRes && $storedRes->num_rows > 0) {
            $passwordPlain = $storedRes->fetch_assoc()['plain_password'];
        } else {
            // Генерируем новый пароль (10 символов) из A-W, a-w, 0-9
            $charset = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw0123456789';
            $passwordPlain = '';
            for ($i = 0; $i < 10; $i++) {
                $passwordPlain .= $charset[random_int(0, strlen($charset) - 1)];
            }
        }
        $password = $passwordPlain; // для хэша
        $confirm_password = $passwordPlain; // чтобы пройти старую валидацию
        
        // Validation
        if (empty($username)) {
            $error = 'Пожалуйста, заполните все поля';

        } else {
            // Check if user exists
            $check = $conn->prepare("SELECT COUNT(*) as count FROM litebans_users WHERE username = ?");
            $check->bind_param("s", $username);
            $check->execute();
            $result = $check->get_result();
            $userExists = $result->fetch_assoc()['count'] > 0;
            
            if ($userExists) {
                $error = "Помощник с именем $username уже существует";
            } else {
                // Проверяем лимит 5 человек на выбранный ранг
                $cntRole = $conn->prepare("SELECT COUNT(*) as c FROM litebans_users WHERE role=?");
                $cntRole->bind_param("s", $role);
                $cntRole->execute();
                $rc = $cntRole->get_result()->fetch_assoc()['c'] ?? 0;

                if ($rc >= 5) {
                    $error = "Лимит 5 членов для ранга $role достигнут";
                } else {
                    $hashed_password = password_hash($passwordPlain, PASSWORD_DEFAULT);

                    // Insert helper
                    $insert = $conn->prepare("INSERT INTO litebans_users (username, password, plain_password, role) VALUES (?, ?, ?, ?)");
                    $insert->bind_param("ssss", $username, $hashed_password, $passwordPlain, $role);

                    if ($insert->execute()) {
                        // Сохраняем пароль в историю
                        $hist = $conn->prepare("INSERT INTO helper_passwords (username, plain_password) VALUES (?, ?) ON DUPLICATE KEY UPDATE plain_password = VALUES(plain_password)");
                        $hist->bind_param("ss", $username, $passwordPlain);
                        $hist->execute();
                        // Очистим старые warns, если были
                        // 1) staff_warns
                        $delWarn = $conn->prepare('DELETE FROM staff_warns WHERE staff_username=?');
                        $delWarn->bind_param('s', $username);
                        $delWarn->execute();
                        // 2) активные litebans_warnings
                        $uuidStmt = $conn->prepare('SELECT uuid FROM litebans_history WHERE name=? ORDER BY date DESC LIMIT 1');
                        $uuidStmt->bind_param('s',$username);
                        $uuidStmt->execute();
                        $uuidRes = $uuidStmt->get_result();
                        if($uuidRes && $uuidRes->num_rows){
                            $uuid = $uuidRes->fetch_assoc()['uuid'];
                            $updWarn = $conn->prepare("UPDATE litebans_warnings SET active=b'0', removed_by_name='AdminPanel', removed_by_reason='Cleared on re-add', removed_by_date=NOW() WHERE uuid=? AND active=b'1'");
                            $updWarn->bind_param('s',$uuid);
                            $updWarn->execute();
                        }

                        $generated_password = $passwordPlain;
                        $success = "Помощник $username ($role) успешно добавлен! Пароль: <span class='generated-pass'>$generated_password</span> <button class='copy-btn' data-password='$generated_password'>Копировать</button>";
                    } else {
                        $error = "Ошибка при добавлении помощника: " . $insert->error;
                    }

                    $insert->close();
                }
            }
                    
        }
        
        $check->close();
    }
    elseif ($_POST['action'] === 'delete' && isset($_POST['id'])) {
        header('Content-Type: application/json; charset=utf-8');
        $helper_id = intval($_POST['id']);
        
        // Получаем информацию о пользователе
        $stmt = $conn->prepare("SELECT username, plain_password FROM litebans_users WHERE id = ?");
        $stmt->bind_param("i", $helper_id);
        $stmt->execute();
        $res = $stmt->get_result();
        
        if ($res && $res->num_rows === 1) {
            $row = $res->fetch_assoc();
            // Сохраняем пароль, если был
            if (!empty($row['plain_password'])) {
                $save = $conn->prepare("INSERT INTO helper_passwords (username, plain_password) VALUES (?, ?) ON DUPLICATE KEY UPDATE plain_password = VALUES(plain_password)");
                $save->bind_param("ss", $row['username'], $row['plain_password']);
                $save->execute();
            }
            // Удаляем пользователя
            $del = $conn->prepare("DELETE FROM litebans_users WHERE id = ?");
            $del->bind_param("i", $helper_id);
            $success = $del->execute();
            echo json_encode(['success' => $success]);
        } else {
            echo json_encode(['success' => false, 'error' => 'not_found']);
        }
        exit;
    }
    elseif ($_POST['action'] === 'refresh_password' && isset($_POST['id'])) {
        header('Content-Type: application/json; charset=utf-8');
        $helper_id = intval($_POST['id']);
        
        // Генерируем новый пароль
        $charset = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw0123456789';
        $newPass = '';
        for ($i = 0; $i < 10; $i++) { $newPass .= $charset[random_int(0, strlen($charset) - 1)]; }
        $hash = password_hash($newPass, PASSWORD_DEFAULT);
        
        // Обновляем запись
        $upd = $conn->prepare("UPDATE litebans_users SET password=?, plain_password=? WHERE id = ?");
        $upd->bind_param("ssi", $hash, $newPass, $helper_id);
        $ok = $upd->execute();
        if ($ok) {
            // Обновляем таблицу historical passwords
            $save = $conn->prepare("INSERT INTO helper_passwords (username, plain_password) SELECT username, ? FROM litebans_users WHERE id = ? ON DUPLICATE KEY UPDATE plain_password = VALUES(plain_password)");
            $save->bind_param("si", $newPass, $helper_id);
            $save->execute();
            echo json_encode(['success' => true, 'password' => $newPass, 'mask' => substr($newPass,0,3).'***']);
        } else {
            echo json_encode(['success' => false]);
        }
        exit;
}

}

// Get list of helpers & staff (include guardian field)
$helpers = $conn->query("SELECT u.id, u.username, u.plain_password, u.role, u.parent_username, u.created_at,
    (
        SELECT COUNT(*)
        FROM litebans_warnings w
        WHERE w.active = b'1'
          AND (
                SELECT name COLLATE utf8mb4_unicode_ci
                FROM litebans_history
                WHERE uuid = w.uuid
                ORDER BY date DESC LIMIT 1
              ) = u.username COLLATE utf8mb4_unicode_ci
    ) + COALESCE(sw.warn_count,0) AS warn_count
FROM litebans_users u
LEFT JOIN staff_warns sw ON sw.staff_username = u.username
WHERE u.role IN ('owner','investor','admin','mod','helper')
ORDER BY u.created_at DESC");
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Управление помощниками - LiteBans Админ панель</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:1000;}
.modal-overlay.hidden{display:none;}
.modal-content{background:#fff;padding:20px;border-radius:6px;max-width:300px;width:90%;box-shadow:0 4px 16px rgba(0,0,0,.3);}
.modal-actions{margin-top:15px;display:flex;gap:10px;justify-content:flex-end;}
.btn-primary{background:#d9534f;color:#fff;border:none;padding:6px 14px;cursor:pointer;border-radius:4px;}
.btn-secondary{background:#6c757d;color:#fff;border:none;padding:6px 14px;cursor:pointer;border-radius:4px;}
.helper-actions form {
            display: inline-block;
        }
        .delete-btn {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        .helper-list {
            margin-top: 20px;
            width: 100%;
            border-collapse: collapse;
        }
        .helper-list th, .helper-list td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .helper-list th {
            background-color: #f2f2f2;
        }
        .helper-list tr:hover {
            background-color: #f5f5f5;
        }
        .pwd-mask {
            font-family: monospace;
            background-color: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .copy-btn {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 4px;
        }
        .copy-btn:hover { opacity: .85; }
        .refresh-btn{
            background-color:#6c757d;
            border:none;
            color:#fff;
            padding:2px 6px;
            border-radius:4px;
        }
        select.role-select {
            padding: 4px 6px;
            border-radius: 4px;
            border: 1px solid #ccc;
            font-size: 13px;
        }
        .add-helper-form {
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Управление помощниками</h1>
        
        <div class="nav-links">
            <a href="index.php">← Вернуться в админ панель</a>
        </div>
        
        <?php if (!empty($success)): ?>
            <div class="message success-message"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <?php if (!empty($error)): ?>
            <div class="message error-message"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <!-- Add helper form -->
        <div class="add-helper-form">
            <h2>Добавить нового помощника</h2>
            <form method="POST" action="">
                <input type="hidden" name="action" value="add">
                <div class="form-group">
                    <label for="username">Имя помощника:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="role">Ранг:</label>
                    <select id="role" name="role" required>
                        <option value="owner">Owner</option>
                        <option value="investor">Investor</option>
                        <option value="admin">Admin</option>
                        <option value="mod">Mod</option>
                        <option value="helper" selected>Helper</option>
                    </select>
                </div>
                <p>Пароль будет сгенерирован автоматически и показан после создания помощника.</p>
                
                <div class="form-group">
                    <button type="submit" class="btn-primary">Добавить помощника</button>
                </div>
            </form>
        </div>
        
        <!-- Helpers list -->
        <h2>Список помощников</h2>
        <?php if ($helpers->num_rows > 0): ?>
            <table class="helper-list">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Имя</th>
                        <th>Ранк</th>
                        <th>Опекун</th>
                        <th>Warns</th>
                        <th>Пароль</th>
                        <th>Дата создания</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($helper = $helpers->fetch_assoc()): ?>
                        <tr>
                            <td><?php echo $helper['id']; ?></td>
                            <td><?php echo htmlspecialchars($helper['username']); ?></td>
                            <td>
                                <select class="role-select" data-id="<?php echo $helper['id']; ?>">
                                    <option value="owner" <?php if($helper['role']==='owner') echo 'selected'; ?>>Owner</option>
                                    <option value="investor" <?php if($helper['role']==='investor') echo 'selected'; ?>>Investor</option>
                                    <option value="admin" <?php if($helper['role']==='admin') echo 'selected'; ?>>Admin</option>
                                    <option value="mod" <?php if($helper['role']==='mod') echo 'selected'; ?>>Mod</option>
                                    <option value="helper" <?php if($helper['role']==='helper') echo 'selected'; ?>>Helper</option>
                                </select>
                                <?php 
                                    $roleGradients = [
                                    'owner' => ['#ff0000','#a80000'],
                                    'investor' => ['#03ad2b','#03ad2b'],
                                    'admin' => ['#00ffd9','#03a38b'],
                                    'mod' => ['#9d00ff','#7c04b0'],
                                    'helper' => ['#00ffff','#0285d1']
                                ];
                                $grad = $roleGradients[$helper['role']] ?? ['#0285d1','#0285d1'];
                                $roleStyle = "linear-gradient(45deg, {$grad[0]}, {$grad[1]})";
                                ?>
                                <span class="role-badge" style="background: <?php echo $roleStyle; ?>; color:#fff; padding:2px 6px; border-radius:4px; font-size:12px; font-weight:600; margin-left:4px;">
                                    <?php echo ucfirst($helper['role']); ?>
                                </span>
                             </td>
                             <td>
                                 <?php if($helper['role']==='helper'): ?>
                                     <select class="parent-select" data-id="<?php echo $helper['id']; ?>">
                                         <option value="">—</option>
                                         <?php foreach($adminUsernames as $adminName): ?>
                                              <?php if($adminName === $helper['parent_username'] || !in_array($adminName,$guardiansTaken)): ?>
                                                  <option value="<?php echo $adminName; ?>" <?php if($helper['parent_username']===$adminName) echo 'selected'; ?>><?php echo htmlspecialchars($adminName); ?></option>
                                              <?php endif; ?>
                                         <?php endforeach; ?>
                                     </select>
                                     <?php if(!empty($helper['parent_username'])): ?>
                                         <span class="parent-badge" style="background:linear-gradient(45deg,#00fcce,#00b896);color:#fff;padding:2px 6px;border-radius:4px;font-size:12px;font-weight:600;margin-left:4px;">
                                             <?php echo htmlspecialchars($helper['parent_username']); ?>
                                         </span>
                                     <?php endif; ?>
                                 <?php else: ?>
                                     <?php echo !empty($helper['parent_username']) ? htmlspecialchars($helper['parent_username']) : '—'; ?>
                                 <?php endif; ?>
                             </td>
                             <td>
                                <?php echo $helper['warn_count']; ?>
                                <button class="clear-warn-btn" data-id="<?php echo $helper['id']; ?>" title="Очистить">🧹</button>
                             </td>
                             <td>
                                <?php if(!empty($helper['plain_password'])): ?>
                                    <span id="pwd-<?php echo $helper['id']; ?>" class="pwd-mask"><?php echo htmlspecialchars(substr($helper['plain_password'],0,3)); ?>***</span>
                                    <button class="copy-btn" data-password="<?php echo htmlspecialchars($helper['plain_password']); ?>" title="Копировать">📋</button>
                                    <button class="refresh-btn" data-id="<?php echo $helper['id']; ?>" title="Обновить пароль">🔄</button>
                                <?php else: ?>—<?php endif; ?>
                             </td>
                             <td><?php echo $helper['created_at']; ?></td>
                             <td class="helper-actions">
                                 <button class="delete-btn" data-id="<?php echo $helper['id']; ?>">Удалить</button>
                             </td>
                         </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p>Помощники не найдены.</p>
        <?php endif; ?>
    </div>

<!-- Confirmation Modal -->
<div id="confirmModal" class="modal-overlay hidden">
    <div class="modal-content">
        <p>Вы уверены, что хотите удалить помощника?</p>
        <div class="modal-actions">
            <button id="confirmDeleteBtn" class="btn-primary">Удалить</button>
            <button id="cancelDeleteBtn" class="btn-secondary">Отмена</button>
        </div>
    </div>
</div>
<script>
    let deletingId = null;

    document.addEventListener('click', (e) => {
        const t = e.target;

        // Copy password
        if (t.classList.contains('copy-btn')) {
            const pass = t.dataset.password;
            navigator.clipboard.writeText(pass).then(() => {
                const prev = t.textContent;
                t.textContent = '✓';
                setTimeout(() => { t.textContent = prev; }, 1500);
            });
        }
        // Refresh password
        else if (t.classList.contains('refresh-btn')) {
            const id = t.dataset.id;
            fetch('', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
                body: `action=refresh_password&id=${id}`
            }).then(r => r.json()).then(res => {
                if (res.success) {
                    const span = document.getElementById(`pwd-${id}`);
                    if (span) span.textContent = res.mask;
                    const copyBtn = t.parentElement.querySelector('.copy-btn');
                    if (copyBtn) copyBtn.dataset.password = res.password;
                }
            });
        }
        // Delete helper
        else if (t.classList.contains('delete-btn')) {
            deletingId = t.dataset.id;
            document.getElementById('confirmModal').classList.remove('hidden');
        }
        // Cancel modal
        else if (t.id === 'cancelDeleteBtn') {
            document.getElementById('confirmModal').classList.add('hidden');
            deletingId = null;
        }
        // Confirm delete
        else if (t.id === 'confirmDeleteBtn' && deletingId) {
            fetch('', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
                body: `action=delete&id=${deletingId}`
            }).then(r => r.json()).then(res => {
                if (res.success) {
                    const row = document.querySelector(`button.delete-btn[data-id="${deletingId}"]`)?.closest('tr');
                    if (row) row.remove();
                }
                document.getElementById('confirmModal').classList.add('hidden');
                deletingId = null;
            });
        }
    });

    // Role/Parent change handler
    document.addEventListener('change', (e) => {
        if (e.target.classList.contains('role-select')) {
            const id = e.target.dataset.id;
            const role = e.target.value;
            fetch('', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
                body: `action=update_role&id=${id}&role=${role}`
            }).then(r=>r.json()).then(res=>{
                if(res && res.success===false && res.message==='limit'){
                    alert('Лимит 5 членов для выбранного ранга уже достигнут');
                    // revert select value to previous (reload page simplest)
                    window.location.reload();
                    return;
                }
                const badge = e.target.nextElementSibling;
                const gradients = {
                    owner: 'linear-gradient(45deg, #ff0000, #a80000)',
                    investor: 'linear-gradient(45deg, #03ad2b, #03ad2b)',
                    admin: 'linear-gradient(45deg, #00ffd9, #03a38b)',
                    mod: 'linear-gradient(45deg, #9d00ff, #7c04b0)',
                    helper: 'linear-gradient(45deg, #00ffff, #0285d1)'
                };
                badge.style.background = gradients[role] || gradients.helper;
                badge.textContent = role.charAt(0).toUpperCase() + role.slice(1);
            });
        }
    });

    // Guardian (parent) select change
    document.addEventListener('change', (e)=>{
        if(e.target.classList.contains('parent-select')){
            const id = e.target.dataset.id;
            const parent = e.target.value;
            fetch('',{
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
                body:`action=update_parent&id=${id}&parent=${encodeURIComponent(parent)}`
            }).then(()=>{
                // Update badge next to select
                let badge = e.target.parentElement.querySelector('.parent-badge');
                if(parent){
                    if(!badge){
                        badge = document.createElement('span');
                        badge.className='parent-badge';
                        badge.style.background='linear-gradient(45deg,#00fcce,#00b896)';
                        badge.style.color='#fff';
                        badge.style.padding='2px 6px';
                        badge.style.borderRadius='4px';
                        badge.style.fontSize='12px';
                        badge.style.fontWeight='600';
                        badge.style.marginLeft='4px';
                        e.target.parentElement.appendChild(badge);
                    }
                    badge.textContent = parent;
                }else if(badge){
                    badge.remove();
                }
            });
        }
    });
    // Clear warn button
    document.addEventListener('click',(e)=>{
        if(e.target.classList.contains('clear-warn-btn')){
            const id = e.target.dataset.id;
            fetch('api/clear_warns.php',{
              method:'POST',
              headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
              body:`id=${id}`
            }).then(r=>r.json()).then(res=>{
               if(res.success){
                   // set warn count cell to 0
                   e.target.parentElement.firstChild.textContent='0';
               }
            });
        }
    });

    // periodic warn checker
    setInterval(()=>{ fetch('api/check_warns.php').catch(()=>{}); },10000);
</script>
</body>
</html>
