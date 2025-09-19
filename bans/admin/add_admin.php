<?php
include 'db_config.php';

// Данные администратора
$username = 'limon1232';
$password = 'xoji2859447';

// Хеширование пароля
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// Проверка, существует ли уже пользователь с таким именем
$check = $conn->prepare("SELECT COUNT(*) as count FROM litebans_users WHERE username = ?");
$check->bind_param("s", $username);
$check->execute();
$result = $check->get_result();
$userExists = $result->fetch_assoc()['count'] > 0;

if ($userExists) {
    echo "Администратор с именем $username уже существует. Обновляем пароль...";
    
    // Обновляем пароль существующего пользователя
    $update = $conn->prepare("UPDATE litebans_users SET password = ? WHERE username = ?");
    $update->bind_param("ss", $hashed_password, $username);
    
    if ($update->execute()) {
        echo "<p>Пароль администратора успешно обновлен!</p>";
    } else {
        echo "<p>Ошибка при обновлении пароля: " . $update->error . "</p>";
    }
    
    $update->close();
} else {
    // Добавляем нового администратора
    $insert = $conn->prepare("INSERT INTO litebans_users (username, password) VALUES (?, ?)");
    $insert->bind_param("ss", $username, $hashed_password);
    
    if ($insert->execute()) {
        echo "<p>Администратор $username успешно добавлен!</p>";
    } else {
        echo "<p>Ошибка при добавлении администратора: " . $insert->error . "</p>";
    }
    
    $insert->close();
}

echo "<p><a href='login.php'>Перейти на страницу входа</a></p>";
?>
