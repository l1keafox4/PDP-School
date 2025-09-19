<?php
// get_staff_guardians.php
// Returns mapping of helper username (lowercase) to its guardian (parent_username)
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once '../admin/db_config.php';

$guardians = [];
$res = $conn->query("SELECT username, parent_username FROM litebans_users WHERE role='helper' AND parent_username IS NOT NULL AND parent_username != ''");
if($res){
    while($row = $res->fetch_assoc()){
        $guardians[strtolower($row['username'])] = $row['parent_username'];
    }
}

echo json_encode($guardians);
$conn->close();
?>
