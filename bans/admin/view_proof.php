<?php
include 'auth.php';
include 'db_config.php';

// Проверка параметров
if (!isset($_GET['type']) || !isset($_GET['id'])) {
    header('Location: manage_proofs.php');
    exit;
}

$type = $_GET['type'];
$id = (int)$_GET['id'];

// Получение информации о пруфе
if ($type === 'ban') {
    $stmt = $conn->prepare("
        SELECT p.*, b.uuid, b.reason, b.banned_by_name, b.time 
        FROM litebans_proof p 
        LEFT JOIN litebans_bans b ON p.ban_id = b.id 
        WHERE p.id = ?
    ");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $proof = $stmt->get_result()->fetch_assoc();
    
    if (!$proof) {
        header('Location: manage_proofs.php');
        exit;
    }
    
    // Преобразование для унификации отображения
    $proof['punishment_id'] = $proof['ban_id'];
    $proof['punishment_type'] = 'ban';
} elseif ($type === 'mute') {
    $stmt = $conn->prepare("
        SELECT p.*, m.uuid, m.reason, m.banned_by_name, m.time 
        FROM litebans_mute_proof p 
        LEFT JOIN litebans_mutes m ON p.mute_id = m.id 
        WHERE p.id = ?
    ");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $proof = $stmt->get_result()->fetch_assoc();
    
    if (!$proof) {
        header('Location: manage_proofs.php');
        exit;
    }
    
    // Преобразование для унификации отображения
    $proof['punishment_id'] = $proof['mute_id'];
    $proof['punishment_type'] = 'mute';
} else {
    header('Location: manage_proofs.php');
    exit;
}

// Преобразование Unix timestamp в читаемый формат
$date = date('Y-m-d H:i:s', $proof['time'] / 1000);
?>
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dalilni ko'rish - BeastMine Admin panel</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css">
    <style>
        :root {
            --plyr-color-main: #ffcc00; /* accent color */
        }
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Segoe UI', Tahoma, sans-serif;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .navbar {
            background-color: #222461;
            border-bottom: 3px solid #ffcc00;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar h1 {
            margin: 0;
            color: #fff;
            font-size: 24px;
        }
        
        .navbar ul {
            display: flex;
            list-style: none;
            gap: 20px;
            margin: 0;
            padding: 0;
        }
        
        .navbar ul li a {
            color: #e6e6e6;
            text-decoration: none;
            transition: color 0.2s;
            padding: 5px 10px;
            border-radius: 4px;
        }
        
        .navbar ul li a:hover {
            color: #ffcc00;
            background-color: rgba(255, 204, 0, 0.1);
        }
        
        .card {
            background-color: #2a2a4a;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .card-header {
            background-color: #292954;
            padding: 15px 20px;
            border-bottom: 1px solid #393963;
            font-weight: bold;
            font-size: 18px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .proof-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .proof-preview {
            max-width: 100%;
            max-height: 600px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        .proof-video {
            max-width: 100%;
            max-height: 600px;
            width: auto;
            height: auto;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
        }
        
        th {
            background-color: #222461;
            color: #e6e6e6;
            font-weight: 600;
        }
        
        td {
            background-color: #2a2a4a;
            border-bottom: 1px solid #393963;
        }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
            margin-right: 10px;
            border: none;
        }
        
        .btn-primary {
            background-color: #ffcc00;
            color: #222;
        }
        
        .btn-primary:hover {
            background-color: #e6b800;
        }
        
        .btn-danger {
            background-color: #ff5252;
            color: white;
        }
        
        .btn-danger:hover {
            background-color: #ff3838;
        }
        
        .admin-name {
            color: #ff5252;
            font-weight: bold;
        }
        
        .player-name {
            color: #ffcc00;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .proof-details {
                grid-template-columns: 1fr;
            }
            
            .navbar {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .navbar ul {
                margin-top: 15px;
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>BeastMine Admin panel</h1>
        <ul>
            <li><a href="index.php">Asosiy</a></li>
            <li><a href="upload_proof.php">Dalillarni yuklash</a></li>
            <li><a href="manage_proofs.php">Dalillarni boshqarish</a></li>
            <li><a href="logout.php">Chiqish</a></li>
        </ul>
    </div>

    <div class="container">
        <h2>Dalilni ko'rish #<?php echo $id; ?></h2>
        
        <div class="card">
            <div class="card-header">Jazo va dalil ma'lumotlari</div>
            <div class="card-body">
                <div class="proof-details">
                    <div>
                        <h3 class="admin-name">Jazo ma'lumotlari</h3>
                        <table>
                            <tr>
                                <th>Jazo turi</th>
                                <td><?php echo $proof['punishment_type'] === 'ban' ? 'Ban' : 'Mute'; ?></td>
                            </tr>
                            <tr>
                                <th>Jazo ID</th>
                                <td><?php echo $proof['punishment_id']; ?></td>
                            </tr>
                            <?php 
                            // Получаем имя игрока из истории по UUID
                            $player_query = $conn->prepare("SELECT name FROM litebans_history WHERE uuid = ? ORDER BY date DESC LIMIT 1");
                            $player_query->bind_param("s", $proof['uuid']);
                            $player_query->execute();
                            $player_result = $player_query->get_result();
                            $player_name = $player_result->num_rows > 0 ? $player_result->fetch_assoc()['name'] : $proof['uuid'];
                            ?>
                            <tr>
                                <th>O'yinchi</th>
                                <td><span class="player-name"><?php echo htmlspecialchars($player_name); ?></span> <span style="color: #aaa; font-size: 12px;">(<?php echo htmlspecialchars($proof['uuid']); ?>)</span></td>
                            </tr>
                            <tr>
                                <th>Sabab</th>
                                <td><?php echo htmlspecialchars($proof['reason']); ?></td>
                            </tr>
                            <tr>
                                <th>Admin</th>
                                <td><span class="admin-name"><?php echo htmlspecialchars($proof['banned_by_name']); ?></span></td>
                            </tr>
                            <tr>
                                <th>Sana</th>
                                <td><?php echo $date; ?></td>
                            </tr>
                        </table>
                    </div>
                    
                    <div>
                        <h3 class="player-name">Dalil ma'lumotlari</h3>
                        <table>
                            <tr>
                                <th>Dalil ID</th>
                                <td><?php echo $id; ?></td>
                            </tr>
                            <tr>
                                <th>Dalil turi</th>
                                <td><?php echo $proof['proof_type'] === 'image' ? 'Rasm' : 'Video'; ?></td>
                            </tr>
                            <tr>
                                <th>Yuklangan sana</th>
                                <td><?php echo $proof['uploaded_at']; ?></td>
                            </tr>
                            <tr>
                                <th>Dalil manzili</th>
                                <td>
                                    <a href="<?php echo '../' . htmlspecialchars($proof['proof_url']); ?>" target="_blank" style="color: #ffcc00;">
                                        <?php echo htmlspecialchars($proof['proof_url']); ?>
                                    </a>
                                </td>
                            </tr>
                        </table>
                        
                        <div style="margin-top: 20px;">
                            <a href="manage_proofs.php?action=delete&type=<?php echo $proof['punishment_type']; ?>&id=<?php echo $id; ?>" class="btn btn-danger" onclick="return confirm('Ushbu dalilni o\'chirishni xohlaysizmi?')">Dalilni o'chirish</a>
                            <a href="manage_proofs.php" class="btn btn-primary">Ro'yxatga qaytish</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">Dalil ko'rinishi</div>
            <div class="card-body" style="text-align: center;">
                <?php if ($proof['proof_type'] === 'image'): ?>
                    <img src="<?php echo '../' . htmlspecialchars($proof['proof_url']); ?>" alt="Dalil" class="proof-preview">
                <?php elseif ($proof['proof_type'] === 'video'): ?>
                    <video controls class="proof-video" id="player">
                        <source src="<?php echo '../' . htmlspecialchars($proof['proof_url']); ?>" type="video/mp4">
                        Sizning brauzeringiz videoni qo'llab-quvvatlamaydi.
                    </video>
                <?php endif; ?>
            </div>
        </div>
    </div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const player = new Plyr('#player', {
                controls: ['play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen'],
                ratio: '16:9'
            });
        });
    </script>
</body>
</html>
