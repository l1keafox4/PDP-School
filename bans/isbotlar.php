<?php
include 'admin/db_config.php';

// Инициализация массива для хранения доказательств
$proofs = [];
$error_message = '';

// Проверяем наличие таблиц
$tables_check = $conn->query("SHOW TABLES LIKE 'litebans_proof'");
$mute_tables_check = $conn->query("SHOW TABLES LIKE 'litebans_mute_proof'");

if (!$tables_check || $tables_check->num_rows == 0) {
    // Таблица litebans_proof не существует, создаем её
    $create_table_sql = "CREATE TABLE IF NOT EXISTS litebans_proof (
        id INT(11) NOT NULL AUTO_INCREMENT,
        ban_id BIGINT(20) UNSIGNED NOT NULL,
        proof_url VARCHAR(2048) NOT NULL,
        proof_type VARCHAR(50) NOT NULL,
        admin_feedback TEXT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY ban_id (ban_id)
    )";
    
    if ($conn->query($create_table_sql) !== TRUE) {
        $error_message .= "\u041eшибка при создании таблицы litebans_proof: " . $conn->error . "<br>";
    }
}

if (!$mute_tables_check || $mute_tables_check->num_rows == 0) {
    // Таблица litebans_mute_proof не существует, создаем её
    $create_mute_table_sql = "CREATE TABLE IF NOT EXISTS litebans_mute_proof (
        id INT(11) NOT NULL AUTO_INCREMENT,
        mute_id BIGINT(20) UNSIGNED NOT NULL,
        proof_url VARCHAR(2048) NOT NULL,
        proof_type VARCHAR(50) NOT NULL,
        admin_feedback TEXT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY mute_id (mute_id)
    )";
    
    if ($conn->query($create_mute_table_sql) !== TRUE) {
        $error_message .= "\u041eшибка при создании таблицы litebans_mute_proof: " . $conn->error . "<br>";
    }
}

// Получаем список доказательств с комментариями админа
try {
    $query = "
        SELECT 
            p.id,
            p.ban_id,
            p.proof_url,
            p.proof_type,
            p.created_at,
            p.admin_feedback,
            b.reason,
            b.banned_by_name,
            (SELECT h.name FROM litebans_history h WHERE h.uuid = b.uuid ORDER BY h.date DESC LIMIT 1) AS player_name
        FROM 
            litebans_proof p
        JOIN 
            litebans_bans b ON p.ban_id = b.id
        ORDER BY 
            p.created_at DESC
    ";

    $result = $conn->query($query);
    
    if (!$result) {
        $error_message .= "SQL ошибка при запросе доказательств банов: " . $conn->error . "<br>";
    } else if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $proofs[] = $row;
        }
    }
} catch (Exception $e) {
    $error_message .= "Исключение при запросе доказательств банов: " . $e->getMessage() . "<br>";
}

// Также получаем доказательства по мутам
try {
    $query_mutes = "
        SELECT 
            p.id,
            p.mute_id AS ban_id,
            p.proof_url,
            p.proof_type,
            p.created_at,
            p.admin_feedback,
            m.reason,
            m.banned_by_name,
            (SELECT h.name FROM litebans_history h WHERE h.uuid = m.uuid ORDER BY h.date DESC LIMIT 1) AS player_name
        FROM 
            litebans_mute_proof p
        JOIN 
            litebans_mutes m ON p.mute_id = m.id
        ORDER BY 
            p.created_at DESC
    ";

    $result_mutes = $conn->query($query_mutes);
    
    if (!$result_mutes) {
        $error_message .= "SQL ошибка при запросе доказательств мутов: " . $conn->error . "<br>";
    } else if ($result_mutes->num_rows > 0) {
        while ($row = $result_mutes->fetch_assoc()) {
            $proofs[] = $row;
        }
    }
} catch (Exception $e) {
    $error_message .= "Исключение при запросе доказательств мутов: " . $e->getMessage() . "<br>";
}

// Сортируем все доказательства по дате (от новых к старым)
usort($proofs, function($a, $b) {
    return strtotime($b['created_at']) - strtotime($a['created_at']);
});
?>

<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Isbotlar - BeastMine</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon@4.1.0/fonts/remixicon.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css">
    <style>
        @font-face {
            font-family: 'Berlin Sans FB Demi';
            src: url('/fonts/BRLNSDB.woff2') format('woff2');
            font-weight: bold;
            font-style: normal;
        }
        
        :root {
            --plyr-color-main: #e94560; /* accent for player */
            --primary-dark: #1a1a2e;
            --secondary-dark: #16213e;
            --accent-color: #0f3460;
            --highlight: #e94560;
            --text-light: #f5f5f5;
            --text-dim: #b0b0b0;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--primary-dark);
            color: var(--text-light);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header h1 {
            font-family: 'Berlin Sans FB Demi', sans-serif;
            color: var(--text-light);
            letter-spacing: 1px;
        }
        
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-light);
            text-decoration: none;
            padding: 0.5rem 1rem;
            background-color: var(--accent-color);
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background-color: var(--highlight);
        }
        
        .proofs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }
        
        .proof-card {
            background-color: var(--secondary-dark);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }
        
        .proof-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }
        
        .proof-header {
            padding: 1rem;
            background-color: var(--accent-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .proof-date {
            font-size: 0.9rem;
            color: var(--text-dim);
        }
        
        .proof-type {
            font-size: 0.8rem;
            font-weight: bold;
            color: white;
            background-color: var(--highlight);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
        }
        
        .proof-content {
            padding: 1rem;
        }
        
        .proof-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        .proof-video {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
            width: 100%;
            height: 200px;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        .proof-path {
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-bottom: 1rem;
            word-break: break-all;
        }
        
        .proof-info {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .proof-player, .proof-admin, .proof-reason {
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .info-label {
            color: var(--text-dim);
            font-weight: 500;
        }
        
        .admin-feedback {
            margin-top: 1rem;
            padding: 1rem;
            background-color: rgba(15, 52, 96, 0.5);
            border-radius: 4px;
            border-left: 3px solid var(--highlight);
        }
        
        .feedback-header {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--highlight);
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-dim);
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 100;
            padding: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        
        .modal.show {
            opacity: 1;
            pointer-events: auto;
        }
        
        .modal-content {
            max-width: 900px;
            margin: 2rem auto;
            background-color: var(--secondary-dark);
            border-radius: 8px;
            padding: 2rem;
            position: relative;
            transform: scale(0.95);
            transition: transform 0.3s ease;
        }
        
        .modal.show .modal-content {
            transform: scale(1);
        }
        
        .close-modal {
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.5rem;
            color: var(--text-light);
            cursor: pointer;
            transition: color 0.3s ease;
        }
        
        .close-modal:hover {
            color: var(--highlight);
        }
        
        .modal-image {
            max-width: 100%;
            max-height: 70vh;
            display: block;
            margin: 0 auto;
            border-radius: 4px;
        }
        
        .modal-video {
            max-width: 100%;
            max-height: 70vh;
            width: auto;
            height: auto;
            object-fit: contain;
            display: block;
            margin: 0 auto;
            border-radius: 4px;
        }
            max-width: 100%;
            max-height: 70vh;
            display: block;
            margin: 0 auto;
            border-radius: 4px;
        }
        
        .modal-info {
            margin-top: 1.5rem;
        }
        
        @media (max-width: 768px) {
            .proofs-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 1rem;
            }
        }
    </style>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Isbotlar</h1>
            <a href="/bans/bans.html" class="back-btn">
                <i class="ri-arrow-left-line"></i> Orqaga
            </a>
        </div>
        
        <?php if (!empty($error_message)): ?>
            <div class="error-state">
                <i class="ri-error-warning-line" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: #e94560;"></i>
                <h3>Isbotlarni yuklashda xatolik yuz berdi</h3>
                <div class="error-details">
                    <?php echo $error_message; ?>
                </div>
                <div style="margin-top: 1rem;">
                    <?php
                    // Проверяем и отображаем дополнительную отладочную информацию
                    echo "Директория для загрузок: " . realpath(dirname(__FILE__) . "/uploads/proofs/") . "<br>";
                    echo "Права доступа: " . (is_writable(dirname(__FILE__) . "/uploads/proofs/") ? "Запись разрешена" : "Запись запрещена") . "<br>";
                    ?>
                </div>
            </div>
        <?php elseif (empty($proofs)): ?>
            <div class="empty-state">
                <i class="ri-file-forbid-line" style="font-size: 3rem; margin-bottom: 1rem; display: block;"></i>
                <h3>Hozircha hech qanday isbot yo'q</h3>
                <p>Jazolanganlar uchun isbotlar qo'shilgandan so'ng, bu yerda ko'rinadi.</p>
            </div>
        <?php else: ?>
            <div class="proofs-grid">
                <?php foreach ($proofs as $proof): ?>
                    <div class="proof-card" onclick="openProofModal('<?php echo $proof['id']; ?>')">
                        <div class="proof-header">
                            <div class="proof-date">
                                <?php echo date("d/m/Y, H:i", strtotime($proof['created_at'])); ?>
                            </div>
                            <div class="proof-type">
                                <?php echo $proof['proof_type']; ?>
                            </div>
                        </div>
                        <div class="proof-content">
                            <?php if ($proof['proof_type'] == 'image'): ?>
                                <img src="/bans/<?php echo $proof['proof_url']; ?>" alt="Proof" class="proof-image">
                            <?php elseif ($proof['proof_type'] == 'video'): ?>
                                <video src="/bans/<?php echo $proof['proof_url']; ?>" class="proof-video" muted loop></video>
                            <?php endif; ?>
                            
                            <div class="proof-path"><?php echo $proof['proof_url']; ?></div>
                            
                            <div class="proof-info">
                                <div class="proof-player">
                                    <span class="info-label">O'yinchi:</span> 
                                    <?php echo htmlspecialchars($proof['player_name']); ?>
                                </div>
                                <div class="proof-admin">
                                    <span class="info-label">Admin:</span> 
                                    <?php echo htmlspecialchars($proof['banned_by_name']); ?>
                                </div>
                                <div class="proof-reason">
                                    <span class="info-label">Sabab:</span> 
                                    <?php echo htmlspecialchars(substr($proof['reason'], 0, 100)); ?>
                                    <?php if (strlen($proof['reason']) > 100): ?>...<?php endif; ?>
                                </div>
                            </div>
                            
                            <?php if (!empty($proof['admin_feedback'])): ?>
                                <div class="admin-feedback">
                                    <div class="feedback-header">Admin fikr-mulohazasi:</div>
                                    <?php echo nl2br(htmlspecialchars($proof['admin_feedback'])); ?>
                                </div>
                            <?php endif; ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
    
    <!-- Modal for proof details -->
    <div id="proofModal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeProofModal()">&times;</span>
            <div id="modalContent"></div>
        </div>
    </div>
    
    <script>
        // Open modal with proof details
        function openProofModal(proofId) {
            const proofCards = document.querySelectorAll('.proof-card');
            let proofCard;
            
            // Find the selected proof card
            proofCards.forEach(card => {
                if (card.querySelector('.proof-content').innerHTML.includes(proofId)) {
                    proofCard = card;
                }
            });
            
            if (proofCard) {
                const modalContent = document.getElementById('modalContent');
                const contentClone = proofCard.querySelector('.proof-content').cloneNode(true);
                
                // Adjust image/video for modal view
                if (contentClone.querySelector('.proof-image')) {
                    contentClone.querySelector('.proof-image').className = 'modal-image';
                } else if (contentClone.querySelector('.proof-video')) {
                    const vid = contentClone.querySelector('.proof-video');
                    vid.className = 'modal-video';
                    vid.setAttribute('controls','');
                    setTimeout(()=>{ new Plyr(vid,{controls:['play','progress','current-time','mute','volume','fullscreen'],ratio:'16:9'}); },0);
                }
                    contentClone.querySelector('.proof-video').className = 'modal-video';
                }
                
                modalContent.innerHTML = '';
                modalContent.appendChild(contentClone);
                
                // Add extra info from the card header
                const headerInfo = document.createElement('div');
                headerInfo.className = 'modal-info';
                headerInfo.innerHTML = `
                    <div class="proof-date">
                        <span class="info-label">Sana:</span> 
                        ${proofCard.querySelector('.proof-date').textContent.trim()}
                    </div>
                `;
                modalContent.appendChild(headerInfo);
                
                // Show the modal with fade-in animation
                document.getElementById('proofModal').classList.add('show');
            }
        }
        
        // Close the modal with fade-out animation
        function closeProofModal() {
            const modal = document.getElementById('proofModal');
            if(!modal) return;
            modal.classList.remove('show');
        }
        
        // Close modal when clicking outside of it
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('proofModal');
            if (event.target === modal) {
                closeProofModal();
            }
        });
    </script>
</body>
</html>
