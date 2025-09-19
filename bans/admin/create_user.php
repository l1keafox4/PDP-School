<?php
include 'db_config.php';

// Проверка, существуют ли уже пользователи
$check = $conn->query("SELECT COUNT(*) as count FROM litebans_users");
$userCount = $check->fetch_assoc()['count'];

// Сообщения
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $confirm_password = $_POST['confirm_password'] ?? '';
    
    // Проверка данных
    if (empty($username) || empty($password) || empty($confirm_password)) {
        $message = '<div class="message error-message">Пожалуйста, заполните все поля</div>';
    } elseif ($password !== $confirm_password) {
        $message = '<div class="message error-message">Пароли не совпадают</div>';
    } else {
        // Хеширование пароля
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        
        // Добавление пользователя
        $stmt = $conn->prepare("INSERT INTO litebans_users (username, password) VALUES (?, ?)");
        $stmt->bind_param("ss", $username, $hashed_password);
        
        if ($stmt->execute()) {
            $message = '<div class="message success-message">Пользователь успешно создан! <a href="login.php">Перейти на страницу входа</a></div>';
        } else {
            $message = '<div class="message error-message">Ошибка при создании пользователя: ' . $stmt->error . '</div>';
        }
        
        $stmt->close();
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Создание пользователя - LiteBans Админ панель</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="login-form">
            <h1>Создание администратора</h1>
            
            <?php if ($userCount > 0): ?>
                <div class="message error-message">
                    Администратор уже создан. Если вы забыли пароль, обратитесь к разработчику.
                </div>
            <?php else: ?>
                <?php echo $message; ?>
                
                <form method="POST" action="">
                    <div class="form-group">
                        <label for="username">Имя пользователя:</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Пароль:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="confirm_password">Подтвердите пароль:</label>
                        <input type="password" id="confirm_password" name="confirm_password" required>
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="btn btn-primary">Создать пользователя</button>
                    </div>
                </form>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
