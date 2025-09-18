<?php
// contact.php - простой обработчик формы
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /');
    exit;
}

// Basic sanitization
$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$message = trim($_POST['message'] ?? '');
$token = trim($_POST['form_token'] ?? '');

// Basic validation
$errors = [];
if (!$name) $errors[] = 'Name required';
if (!$email || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Valid email required';
if (!$message) $errors[] = 'Message required';
if (!$token) $errors[] = 'Invalid token';

if ($errors) {
    // simple display — можно сделать редирект с GET-параметром
    echo "<h2>Ошибки:</h2><ul>";
    foreach ($errors as $err) echo "<li>".htmlspecialchars($err)."</li>";
    echo "</ul><p><a href=\"/\">Вернуться</a></p>";
    exit;
}

// Send (simple). Replace $to with your address
$to = "zokirovjasurbek2008@gmail.com"; // <- поменяй на свой email
$subject = "Новое сообщение с лендинга от " . $name;
$body = "Имя: $name\nEmail: $email\n\nСообщение:\n$message";
$headers = "From: $name <$email>\r\nReply-To: $email\r\n";

// Attempt to send. On many shared hosts this works out-of-the-box.
// If mail() not available, integrate PHPMailer + SMTP.
$sent = @mail($to, $subject, $body, $headers);

if ($sent) {
    echo "<h2>Спасибо!</h2><p>Сообщение отправлено успешно.</p><p><a href=\"/\">Вернуться</a></p>";
} else {
    echo "<h2>Ошибка</h2><p>Не удалось отправить сообщение. Попробуйте позже.</p><p><a href=\"/\">Вернуться</a></p>";
}
