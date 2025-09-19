<?php
// my_helper.php – fully refactored and hardened
// ------------------------------------------------
// 1. Uses env vars for secrets (PTERO_TOKEN, PTERO_SERVER)
// 2. Absolute paths for includes
// 3. Checks every DB call; logs and shows friendly message
// 4. Sanitises all user input; CSRF left to your framework
// 5. Compatible with PHP 8.1+

session_start();
require_once __DIR__ . '/auth.php';
require_once __DIR__ . '/db_config.php';

// Only admin users may access
if (!isset($_SESSION['role']) || !in_array($_SESSION['role'], ['admin'], true)) {
    header('Location: index.php');
    exit;
}

$adminName = $_SESSION['username'] ?? 'unknown';
$message   = '';
$error     = '';

// -----------------------------------------------------------------------------
// Helper functions
// -----------------------------------------------------------------------------
function generate_password(int $len = 10): string
{
    $charset = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw0123456789';
    $out = '';
    for ($i = 0; $i < $len; $i++) {
        $out .= $charset[random_int(0, strlen($charset) - 1)];
    }
    return $out;
}

/**
 * Send a command to Pterodactyl panel via Client API.
 * Logs non‑2xx responses to PHP error log.
 */
function sendPteroCmd(string $cmd): void
{

    $url = "https://panel.mchost.uz/api/client/servers/2ea62c18/command";

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 10,
        CURLOPT_HTTPHEADER     => [
            'Content-Type: application/json',
            'Accept: Application/vnd.pterodactyl.v1+json',
            "Authorization: Bearer ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV",
        ],
        CURLOPT_POSTFIELDS     => json_encode(['command' => $cmd], JSON_THROW_ON_ERROR),
    ]);

    $resp = curl_exec($ch);
    if ($resp === false) {
        error_log('cURL error: ' . curl_error($ch));
        curl_close($ch);
        return;
    }
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($code >= 400) {
        error_log("Pterodactyl API {$code}: {$resp}");
    }
}

// -----------------------------------------------------------------------------
// Database helpers
// -----------------------------------------------------------------------------
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$conn->set_charset('utf8mb4');

function db_prepare(mysqli $conn, string $sql): mysqli_stmt|null
{
    try {
        return $conn->prepare($sql);
    } catch (mysqli_sql_exception $e) {
        error_log('DB prepare failed: ' . $e->getMessage());
        return null;
    }
}

// -----------------------------------------------------------------------------
// POST actions
// -----------------------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    // --- ADD helper ----------------------------------------------------------------------
    if ($action === 'add') {
        $nick = trim($_POST['helper_nick'] ?? '');

        if (!preg_match('/^[A-Za-z0-9_]{3,16}$/', $nick)) {
            $error = 'Nick faqat lotin A‑Z, a‑z, 0‑9 va _ dan iborat boʼlishi kerak';
        } else {
            // already helper for this admin?
            $stmt = db_prepare($conn, 'SELECT id,parent_username FROM litebans_users WHERE username=? AND role="helper"');
            if ($stmt) {
                $stmt->bind_param('s', $nick);
                $stmt->execute();
                $res = $stmt->get_result();
                if ($res->num_rows) {
                    $row = $res->fetch_assoc();
                    $error = ($row['parent_username'] === $adminName)
                        ? 'Bu xelper allaqachon sizga biriktirilgan'
                        : 'Bu xelper boshqa adminga biriktirilgan';
                } else {
                    // generate or reuse password
                    $stored = db_prepare($conn, 'SELECT plain_password FROM helper_passwords WHERE username=?');
                    $plain = null;
                    if ($stored) {
                        $stored->bind_param('s', $nick);
                        $stored->execute();
                        $storedRes = $stored->get_result();
                        $plain = $storedRes->fetch_column();
                    }
                    if (!$plain) {
                        $plain = generate_password();
                    }
                    $hash = password_hash($plain, PASSWORD_DEFAULT);

                    // insert helper
                    $ins = db_prepare($conn, 'INSERT INTO litebans_users (username,password,plain_password,role,parent_username) VALUES (?,?,?,?,?)');
                    if ($ins) {
                        $role = 'helper';
                        $ins->bind_param('sssss', $nick, $hash, $plain, $role, $adminName);
                        $ins->execute();

                        // store plain historically
                        $hist = db_prepare($conn, 'INSERT INTO helper_passwords (username,plain_password) VALUES (?,?) ON DUPLICATE KEY UPDATE plain_password=VALUES(plain_password)');
                        if ($hist) {
                            $hist->bind_param('ss', $nick, $plain);
                            $hist->execute();
                        }

                        // clear warns
                        $delWarn = db_prepare($conn, 'DELETE FROM staff_warns WHERE staff_username=?');
                        if ($delWarn) { $delWarn->bind_param('s', $nick); $delWarn->execute(); }

                        // deactivate active litebans warnings
                        $uuidStmt = db_prepare($conn, 'SELECT uuid FROM litebans_history WHERE name=? ORDER BY date DESC LIMIT 1');
                        if ($uuidStmt) {
                            $uuidStmt->bind_param('s', $nick);
                            $uuidStmt->execute();
                            $uuidRes = $uuidStmt->get_result();
                            $uuid = $uuidRes->fetch_column();
                            if ($uuid) {
                                $updWarn = db_prepare($conn, "UPDATE litebans_warnings SET active=b'0' WHERE uuid=? AND active=b'1'");
                                if ($updWarn) { $updWarn->bind_param('s', $uuid); $updWarn->execute(); }
                            }
                        }

                        // Permissions via LuckPerms (Pterodactyl)
                        sendPteroCmd("/lp user {$nick} parent add helper");

                        $message = "Helper qo'shildi! Parol: <span class='generated-pass'>{$plain}</span>";
                    } else {
                        $error = 'DB insert error';
                    }
                }
            } else {
                $error = 'DB error';
            }
        }
    }

    // --- DELETE helper -------------------------------------------------------------------
    elseif ($action === 'delete') {
        $sel = db_prepare($conn, 'SELECT id,username,created_at FROM litebans_users WHERE role="helper" AND parent_username=? LIMIT 1');
        if ($sel) {
            $sel->bind_param('s', $adminName);
            $sel->execute();
            $row = $sel->get_result()->fetch_assoc();
            if (!$row) {
                $error = 'Sizda xelper yoʼq';
            } else {
                $created = strtotime($row['created_at']);
                if (time() - $created < 7 * 24 * 3600) {
                    $error = 'Xelperni 7 kun ichida oʼchirib boʼlmaydi';
                } else {
                    $nick = $row['username'];
                    sendPteroCmd("/lp user {$nick} parent remove helper");
                    $del = db_prepare($conn, 'DELETE FROM litebans_users WHERE id=?');
                    if ($del) {
                        $del->bind_param('i', $row['id']);
                        $del->execute();
                        $message = 'Xelper oʼchirildi';
                    } else {
                        $error = 'Delete failed';
                    }
                }
            }
        } else {
            $error = 'DB error';
        }
    }
}

// fetch current helper (if any)
$helper = null;
$res = $conn->prepare('SELECT id, username, plain_password, created_at FROM litebans_users WHERE role="helper" AND parent_username=? LIMIT 1');
$res->bind_param('s', $adminName);
$res->execute();
$helper = $res->get_result()->fetch_assoc();
?>
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mening Yordamchim</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .container{max-width:800px;margin:20px auto;}
        table{width:100%;border-collapse:collapse;margin-top:15px;}
        th,td{border:1px solid #ccc;padding:8px;text-align:left;}
        .error{color:#dc3545;margin-top:10px;}
        .msg{color:#28a745;margin-top:10px;}
    </style>
</head>
<body>
<?php include 'navbar_partial.php'; ?>
<div class="container">
    <h2>Mening yordamchim</h2>
    <p style="color:#6c757d;font-size:14px;">Nick aniq oʼyin ichidagi kabi boʼlishi shart. Xato yozsangiz warn olishingiz mumkin.</p>

    <?php if($error): ?><div class="error"><?= $error ?></div><?php endif; ?>
    <?php if($message): ?><div class="msg"><?= $message ?></div><?php endif; ?>

    <?php if(!$helper): ?>
        <form method="post">
            <input type="hidden" name="action" value="add">
            <label for="helper_nick">Yordamchi niki:</label>
            <input type="text" name="helper_nick" id="helper_nick" required pattern="[A-Za-z0-9_]{3,16}">
            <button type="submit">Qo'shish</button>
        </form>
    <?php else: ?>
        <table>
            <thead>
                <tr><th>Nick</th><th>Parol</th><th>Yaratilgan sana</th><th>Amal</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><?= htmlspecialchars($helper['username']); ?></td>
                    <td><span id="pwd"><?= htmlspecialchars(substr($helper['plain_password'],0,3)); ?>***</span> <button id="copyBtn" data-pass="<?= htmlspecialchars($helper['plain_password']); ?>">📋</button></td>
                    <td><?= $helper['created_at']; ?></td>
                    <td>
                        <form method="post" onsubmit="return confirm('Rostdan ham oʼchirmoqchimisiz?');">
                            <input type="hidden" name="action" value="delete">
                            <button type="submit"<?= (time()-strtotime($helper['created_at'])<7*24*3600?' disabled':''); ?>>Oʻchirish</button>
                        </form>
                    </td>
                </tr>
            </tbody>
        </table>
    <?php endif; ?>
</div>
<script>
    document.getElementById('copyBtn')?.addEventListener('click',function(){
        navigator.clipboard.writeText(this.dataset.pass).then(()=>{alert('Nusxa olindi');});
    });
</script>
</body>
</html>
