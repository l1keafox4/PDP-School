<?php
/**
 * staff_warn_processor.php
 *
 *   ▸ Запуск каждые 10 секунд (cron / AJAX)
 *   ▸ Считает предупреждения сотрудникам
 *   ▸ при лимите:
 *       admin  → demote smod → mod
 *       mod    → remove
 *       helper → remove (+ warn админу)
 *   ▸ После демота/удаления:
 *       — сбрасывает все активные LiteBans‑варны
 *       — очищает staff_warns
 */

require_once __DIR__ . '/../db_config.php';

/* ─────────────── CONFIG ─────────────── */
$PTERO_URL   = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command';
$PTERO_TOKEN = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV';

$LIMITS = ['admin' => 3, 'mod' => 2, 'helper' => 1];

/* ───── helper‑таблицы (первый запуск) ───── */
$conn->query("CREATE TABLE IF NOT EXISTS staff_warns (
    staff_username VARCHAR(128) PRIMARY KEY,
    role ENUM('admin','mod','helper') NOT NULL,
    warn_count INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4");

$conn->query("CREATE TABLE IF NOT EXISTS staff_actions_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_username VARCHAR(128),
    staff_role ENUM('admin','mod','helper'),
    action VARCHAR(255),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4");

/* ─────────── Pterodactyl API ─────────── */
function sendCommand(string $cmd, string $url, string $token): bool
{
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 8,
        CURLOPT_HTTPHEADER     => [
            'Authorization: Bearer ' . $token,
            'Content-Type: application/json',
            'Accept: Application/vnd.pterodactyl.v1+json',
        ],
        CURLOPT_POSTFIELDS     => json_encode(['command' => $cmd], JSON_THROW_ON_ERROR),
    ]);
    $resp = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($code >= 400) error_log("Ptero API {$code}: {$resp}");
    curl_close($ch);
    return $code >= 200 && $code < 300;
}

/* ──────────── утилиты ──────────── */
function logAction(mysqli $db, string $user, string $role, string $act, string $details = ''): void
{
    $st = $db->prepare('INSERT INTO staff_actions_log (staff_username, staff_role, action, details) VALUES (?,?,?,?)');
    $st->bind_param('ssss', $user, $role, $act, $details);
    $st->execute();
    $st->close();
}

/** Сброс всех варнов и счётчика для данного игрока */
function clearWarns(mysqli $db, string $playerName): void
{
    /* 1) uuid */
    $uuidSt = $db->prepare('SELECT uuid FROM litebans_history WHERE name=? ORDER BY date DESC LIMIT 1');
    $uuidSt->bind_param('s', $playerName);
    $uuidSt->execute();
    $uuid = $uuidSt->get_result()->fetch_column();
    $uuidSt->close();

    /* 2) LiteBans → inactive */
    if ($uuid) {
        $upd = $db->prepare('UPDATE litebans_warnings SET active=b\'0\' WHERE uuid=? AND active=b\'1\'');
        $upd->bind_param('s', $uuid);
        $upd->execute();
        $upd->close();
    }

    /* 3) staff_warns → удалить строку */
    $del = $db->prepare('DELETE FROM staff_warns WHERE staff_username=?');
    $del->bind_param('s', $playerName);
    $del->execute();
    $del->close();
}

/* ─────────────────── MAIN LOOP ─────────────────── */
$staffRes = $conn->query(
    "SELECT id, username, role, parent_username
     FROM litebans_users
     WHERE role IN ('admin','mod','helper')"
);

while ($staff = $staffRes->fetch_assoc()) {
    $name  = $staff['username'];
    $role  = $staff['role'];
    $limit = $LIMITS[$role] ?? 0;

    /* активные warn‑ы LiteBans */
    $cw = $conn->prepare(
        "SELECT COUNT(*) FROM litebans_warnings w
         JOIN (SELECT uuid FROM litebans_history WHERE name=? ORDER BY date DESC LIMIT 1) h
         ON h.uuid = w.uuid
         WHERE w.active=b'1'"
    );
    $cw->bind_param('s', $name);
    $cw->execute();
    $cw->bind_result($lbWarns);
    $cw->fetch();
    $cw->close();

    /* ручные warn‑ы */
    $rw = 0;
    $mw = $conn->prepare('SELECT warn_count FROM staff_warns WHERE staff_username=?');
    $mw->bind_param('s', $name);
    $mw->execute();
    $r = $mw->get_result()->fetch_assoc();
    if ($r)  $rw = (int)$r['warn_count'];
    $mw->close();

    $warns = $lbWarns + $rw;

    /* превышен лимит? */
    if ($limit && $warns >= $limit) {

        if ($role === 'admin') {
            /* demote smod -> mod */
            sendCommand("lp user {$name} parent remove smod", $PTERO_URL, $PTERO_TOKEN);
            sendCommand("lp user {$name} parent add mod",     $PTERO_URL, $PTERO_TOKEN);

            /* чистим варны прямо сейчас */
            clearWarns($conn, $name);

            /* удаляем его helpers */
            $hSt = $conn->prepare("SELECT id, username FROM litebans_users WHERE role='helper' AND parent_username=?");
            $hSt->bind_param('s', $name);
            $hSt->execute();
            $hl = $hSt->get_result();
            while ($h = $hl->fetch_assoc()) {
                sendCommand("lp user {$h['username']} parent remove helper", $PTERO_URL, $PTERO_TOKEN);
                $conn->query("DELETE FROM litebans_users WHERE id=" . (int)$h['id']);
                logAction($conn, $h['username'], 'helper', 'deleted_due_admin_warn', "admin={$name}");
            }
            $hSt->close();

            /* роль в БД */
            $upd = $conn->prepare("UPDATE litebans_users SET role='mod', parent_username=NULL WHERE id=?");
            $upd->bind_param('i', $staff['id']);
            $upd->execute(); $upd->close();
            logAction($conn, $name, 'admin', 'demoted_to_mod', "warns={$warns}");
        }

        elseif ($role === 'mod') {
            sendCommand("lp user {$name} parent remove mod", $PTERO_URL, $PTERO_TOKEN);
            clearWarns($conn, $name);
            $conn->query("DELETE FROM litebans_users WHERE id=" . (int)$staff['id']);
            logAction($conn, $name, 'mod', 'removed', "warns={$warns}");
        }

        else { /* helper */
            sendCommand("lp user {$name} parent remove helper", $PTERO_URL, $PTERO_TOKEN);
            clearWarns($conn, $name);
            $conn->query("DELETE FROM litebans_users WHERE id=" . (int)$staff['id']);

            /* +1 warn админу */
            if ($staff['parent_username']) {
                $admin = $staff['parent_username'];
                $inc = $conn->prepare(
                    "INSERT INTO staff_warns (staff_username, role, warn_count)
                     VALUES (?,?,1)
                     ON DUPLICATE KEY UPDATE warn_count = warn_count + 1"
                );
                $rRole='admin';
                $inc->bind_param('ss', $admin, $rRole);
                $inc->execute(); $inc->close();
            }
            logAction($conn, $name, 'helper', 'removed_due_warn', "warns={$warns}");
        }
    }
}

echo json_encode(['status' => 'ok']);
