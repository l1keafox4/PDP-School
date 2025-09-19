<?php
/**
 * Скрипт для ручного сброса счетчика нарушений хелпера
 * Вызов: reset_helper_violations.php?helper=имя_хелпера
 */

// Включаем вывод ошибок для отладки
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Настройка пути к лог-файлу
$log_file = __DIR__ . '/../PLUGIN_DEVELOPING/auto_unban_log.txt';

// Функция для логирования
function log_message($message) {
    global $log_file;
    $timestamp = date('[Y-m-d H:i:s]');
    file_put_contents($log_file, "$timestamp $message\n", FILE_APPEND);
}

// Проверка авторизации - доступ только для администраторов
session_start();
if (!isset($_SESSION['username']) || $_SESSION['role'] !== 'admin') {
    echo "Доступ запрещен. Только администраторы могут использовать эту функцию.";
    exit;
}

// Подключение к базе данных
require_once __DIR__ . '/db_config.php';

if (!$conn) {
    echo "Ошибка: Не удалось подключиться к базе данных";
    exit;
}

// Получаем имя хелпера из параметра или формы
$helper_name = isset($_GET['helper']) ? $_GET['helper'] : '';

// Если имя не указано, показываем форму
if (empty($helper_name)) {
    // Получаем список хелперов с нарушениями
    $query = "
        SELECT helper_name, COUNT(*) as violations 
        FROM litebans_helper_violations 
        GROUP BY helper_name 
        ORDER BY violations DESC
    ";
    $result = $conn->query($query);
    $helpers = [];
    
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $helpers[] = $row;
        }
    }
    
    // Выводим HTML-форму
    ?>
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Сброс счетчика нарушений хелпера</title>
        <link rel="stylesheet" href="modern.css">
        <style>
            .container {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .form-control {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .btn {
                padding: 8px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .btn:hover {
                background-color: #0069d9;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .table th, .table td {
                padding: 8px;
                border: 1px solid #ddd;
                text-align: left;
            }
            .table th {
                background-color: #f5f5f5;
            }
            .alert {
                padding: 10px;
                margin-bottom: 15px;
                border-radius: 4px;
            }
            .alert-success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .alert-danger {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Сброс счетчика нарушений хелпера</h1>
            
            <p>Этот инструмент позволяет сбросить счетчик нарушений для хелпера, который не публиковал пруфы вовремя.</p>
            
            <form method="post" action="">
                <div class="form-group">
                    <label for="helper">Имя хелпера:</label>
                    <input type="text" id="helper" name="helper" class="form-control" required>
                </div>
                
                <button type="submit" class="btn" name="reset">Сбросить счетчик</button>
            </form>
            
            <?php if (!empty($helpers)): ?>
                <h2>Хелперы с нарушениями</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Имя хелпера</th>
                            <th>Количество нарушений</th>
                            <th>Действие</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($helpers as $helper): ?>
                            <tr>
                                <td><?php echo htmlspecialchars($helper['helper_name']); ?></td>
                                <td><?php echo $helper['violations']; ?></td>
                                <td>
                                    <a href="?helper=<?php echo urlencode($helper['helper_name']); ?>" class="btn">Сбросить</a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <p>Нет хелперов с зарегистрированными нарушениями.</p>
            <?php endif; ?>
            
            <p><a href="index.php" class="btn" style="background-color: #6c757d;">Вернуться в панель управления</a></p>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// Если имя указано, выполняем сброс счетчика
try {
    // Удаляем все нарушения для указанного хелпера
    $stmt = $conn->prepare("DELETE FROM litebans_helper_violations WHERE helper_name = ?");
    $stmt->bind_param("s", $helper_name);
    $stmt->execute();
    
    $affected_rows = $stmt->affected_rows;
    
    // Логируем операцию
    log_message("Администратор {$_SESSION['username']} сбросил счетчик нарушений для хелпера $helper_name. Удалено записей: $affected_rows");
    
    // Перенаправляем обратно с сообщением об успехе
    header("Location: reset_helper_violations.php?success=1&count=$affected_rows&helper=" . urlencode($helper_name));
    exit;
} catch (Exception $e) {
    // В случае ошибки показываем сообщение
    echo "Произошла ошибка: " . $e->getMessage();
    log_message("Ошибка при сбросе счетчика нарушений: " . $e->getMessage());
}
?>
