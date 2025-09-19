<?php
// Clear warns for staff member (both custom staff_warns counts and litebans_warnings active flags)
// Expects POST id parameter (litebans_users.id)

require_once __DIR__ . '/../db_config.php';
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !isset($_POST['id'])) {
    echo json_encode(['success' => false, 'error' => 'missing_params']);
    exit;
}

$id = intval($_POST['id']);

// fetch username
$stmt = $conn->prepare('SELECT username FROM litebans_users WHERE id = ?');
$stmt->bind_param('i', $id);
$stmt->execute();
$res = $stmt->get_result();
if (!$res || $res->num_rows === 0) {
    echo json_encode(['success' => false, 'error' => 'not_found']);
    exit;
}
$username = $res->fetch_assoc()['username'];

// 1. delete from staff_warns
$del = $conn->prepare('DELETE FROM staff_warns WHERE staff_username = ?');
$del->bind_param('s', $username);
$del->execute();

// 2. find uuid for username from litebans_history (latest record)
$uuidStmt = $conn->prepare('SELECT uuid FROM litebans_history WHERE name = ? ORDER BY date DESC LIMIT 1');
$uuidStmt->bind_param('s', $username);
$uuidStmt->execute();
$uuidRes = $uuidStmt->get_result();
if ($uuidRes && $uuidRes->num_rows === 1) {
    $uuid = $uuidRes->fetch_assoc()['uuid'];
    // mark active warnings as removed
    $upd = $conn->prepare("UPDATE litebans_warnings SET active=b'0', removed_by_name='AdminPanel', removed_by_reason='Cleared via panel', removed_by_date=NOW() WHERE uuid = ? AND active = b'1'");
    $upd->bind_param('s', $uuid);
    $upd->execute();
}

echo json_encode(['success' => true]);
