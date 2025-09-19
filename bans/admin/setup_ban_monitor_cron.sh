#!/bin/bash

# Скрипт для настройки cron задачи для мониторинга банов и пруфов
# Запускать от пользователя, под которым работает веб-сервер (обычно www-data)

# Добавить задачу в crontab для запуска каждые 5 минут
CRON_JOB="*/5 * * * * php /var/www/html/bans/admin/ban_monitor.php > /var/www/html/bans/PLUGIN_DEVELOPING/ban_monitor_output.log 2>&1"

# Путь к текущему скрипту
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Убедиться, что лог-директория существует
mkdir -p "${SCRIPT_DIR}/../PLUGIN_DEVELOPING"

echo "Настройка cron задачи для мониторинга банов и пруфов..."

# Проверяем, существует ли уже такая задача
EXISTING_CRON=$(crontab -l 2>/dev/null | grep "ban_monitor.php")

if [ -n "$EXISTING_CRON" ]; then
    echo "Задача уже существует в crontab:"
    echo "$EXISTING_CRON"
else
    # Добавляем новую задачу
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Задача добавлена в crontab. Мониторинг будет выполняться каждые 5 минут."
fi

echo "Настройка завершена. Логи будут записываться в: ${SCRIPT_DIR}/../PLUGIN_DEVELOPING/ban_activity.log"
