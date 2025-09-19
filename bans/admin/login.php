<?php
session_start();
include 'db_config.php';

// Проверка, авторизован ли пользователь
if(isset($_SESSION['user_id'])) {
    header('Location: index.php');
    exit;
}

// Проверка сообщения об ошибке
if (isset($_GET['error']) && $_GET['error'] === 'account_deleted') {
    $error = 'Ваш аккаунт был удален из системы';
}

// Обработка формы входа
$error = $error ?? '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if (empty($username) || empty($password)) {
        $error = 'Пожалуйста, заполните все поля';
    } else {
        // Проверка учетных данных пользователя
        $stmt = $conn->prepare("SELECT id, username, password, role FROM litebans_users WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows === 1) {
            $user = $result->fetch_assoc();
            
            // Проверка пароля
            if (password_verify($password, $user['password'])) {
                // Успешный вход
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['username'] = $user['username'];
                $_SESSION['role'] = $user['role'] ?? 'admin'; // Default to admin for existing accounts
                
                header('Location: index.php');
                exit;
            } else {
                $error = 'Неверный пароль';
            }
        } else {
            $error = 'Пользователь не найден';
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
    <title>Вход в админ панель</title>
    <link rel="stylesheet" href="style.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .login-form {
            max-width: 400px;
            width: 100%;
            background-color: #2a2a4a;
            padding: 40px 30px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,.4);
        }
        .login-form h1 {
            margin-bottom: 25px;
            text-align: center;
            color: #ffcc00;
        }
        label {
            color: #e6e6e6;
        }
        input[type="text"], input[type="password"] {
            font-size: 1rem;
            padding: 14px 16px;
            background-color: #1f1f37;
            border: 1px solid #444;
            color: #e6e6e6;
        }
        .btn-primary {
            padding: 14px 24px;
            font-size: 1.1rem;
            background-color: #ffcc00;
            color: #1a1a2e;
            font-weight: 600;
            border-radius: 8px;
        }
        .btn-primary:hover { opacity: .9; }
        .error-message {
            background-color: #e94560;
            color: #fff;
            border: none;
        }
    </style>
</head>
<body>
    
        <div class="login-form">
            <h1>Вход в админ панель</h1>
            
            <?php if(!empty($error)): ?>
                <div class="error-message"><?php echo $error; ?></div>
            <?php endif; ?>
            
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
                    <button type="submit" class="btn-primary">Войти</button>
                </div>
            </form>
        </div>
    </body>
</html>
