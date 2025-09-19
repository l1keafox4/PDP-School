<?php
session_start();
include_once 'db_config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

// Initialize role if not set (for backward compatibility)
if (!isset($_SESSION['role'])) {
    $_SESSION['role'] = 'admin'; // Default to admin for existing accounts
}

// ВАЖНО: Проверка существования пользователя в базе данных
// Это предотвратит доступ к админ-панели после удаления аккаунта
if (isset($conn)) {
    $user_id = $_SESSION['user_id'];
    $username = $_SESSION['username'];
    
    $check_user = $conn->prepare("SELECT id FROM litebans_users WHERE id = ? AND username = ?");
    $check_user->bind_param("is", $user_id, $username);
    $check_user->execute();
    $result = $check_user->get_result();
    
    if ($result->num_rows === 0) {
        // Пользователь не найден в базе данных, уничтожаем сессию
        session_unset();
        session_destroy();
        header("Location: login.php?error=account_deleted");
        exit();
    }
}
?>
