#!/bin/bash

# Демон для запуска Python-скрипта мониторинга банов
# Устанавливаем путь к директории скрипта
SCRIPT_DIR="/var/www/html/bans/admin"
LOG_FILE="/var/www/html/bans/PLUGIN_DEVELOPING/ban_daemon.log"

echo "Запуск Python демона мониторинга банов..."
echo "Логи будут записываться в $LOG_FILE"

# Устанавливаем необходимые модули Python, если они отсутствуют
pip3 install mysql-connector-python requests

# Проверяем права на запуск скрипта
if [ ! -x "$SCRIPT_DIR/ban_system.py" ]; then
    chmod +x "$SCRIPT_DIR/ban_system.py"
    echo "Установлены права на выполнение для скрипта"
fi

# Запускаем скрипт Python в фоновом режиме
nohup python3 "$SCRIPT_DIR/ban_system.py" > "$LOG_FILE" 2>&1 &

# Сохраняем PID процесса
PID=$!
echo $PID > "$SCRIPT_DIR/ban_daemon.pid"

echo "Демон запущен (PID: $PID). Логи записываются в $LOG_FILE"
echo "Для остановки демона используйте команду: kill $PID"
