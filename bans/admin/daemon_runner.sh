#!/bin/bash

# Фоновый демон для запуска PHP скриптов каждые 10 секунд
# Автор: Cascade AI, 2025-05-06

# Путь к PHP скриптам
MONITOR_SCRIPT="/var/www/html/bans/admin/ban_monitor.php"
UNBAN_SCRIPT="/var/www/html/bans/admin/auto_unban_checker.php"

# Путь к логам
LOG_DIR="/var/www/html/bans/PLUGIN_DEVELOPING"
DAEMON_LOG="$LOG_DIR/daemon.log"

# Создаем директорию для логов, если не существует
mkdir -p "$LOG_DIR"

# Идентификатор процесса (PID)
PID_FILE="$LOG_DIR/daemon_runner.pid"

# Флаг работы
RUNNING=true

# Функция для корректного завершения работы
cleanup() {
    echo "$(date) [INFO] Получен сигнал завершения. Остановка демона..." >> "$DAEMON_LOG"
    RUNNING=false
    rm -f "$PID_FILE"
    exit 0
}

# Регистрация обработчиков сигналов
trap cleanup SIGINT SIGTERM

# Запуск скрипта с записью в лог
run_script() {
    local script=$1
    local script_name=$(basename "$script")
    echo "$(date) [INFO] Запуск $script_name" >> "$DAEMON_LOG"
    php "$script" >> "$DAEMON_LOG" 2>&1
    local status=$?
    if [ $status -ne 0 ]; then
        echo "$(date) [ERROR] Ошибка выполнения $script_name (код: $status)" >> "$DAEMON_LOG"
    else
        echo "$(date) [INFO] Скрипт $script_name успешно выполнен" >> "$DAEMON_LOG"
    fi
}

# Проверка на уже запущенный экземпляр
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p "$pid" > /dev/null; then
        echo "Демон уже запущен с PID $pid"
        exit 1
    else
        echo "Найден pid-файл устаревшего процесса. Удаление..."
        rm -f "$PID_FILE"
    fi
fi

# Записать PID текущего процесса
echo $$ > "$PID_FILE"

echo "$(date) [INFO] Демон запущен (PID: $$)" >> "$DAEMON_LOG"
echo "Демон запущен (PID: $$). Логи записываются в $DAEMON_LOG"
echo "Для остановки демона используйте команду: kill $(cat $PID_FILE)"

# Основной цикл работы
while $RUNNING; do
    # Запуск скрипта мониторинга банов
    run_script "$MONITOR_SCRIPT"
    
    # Запуск скрипта автоматического разбана
    run_script "$UNBAN_SCRIPT"
    
    # Пауза в 10 секунд
    sleep 10
done

echo "$(date) [INFO] Демон остановлен" >> "$DAEMON_LOG"
rm -f "$PID_FILE"
