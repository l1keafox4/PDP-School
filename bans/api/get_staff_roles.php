<?php
// get_staff_roles.php
// Returns mapping of staff username to role to allow front-end colour badges
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once '../admin/db_config.php';

$roles = [];
$result = $conn->query("SELECT username, role FROM litebans_users WHERE role IN ('owner','investor','admin','mod','helper')");
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $roles[strtolower($row['username'])] = $row['role'];
    }
}

echo json_encode($roles);
$conn->close();
?>
